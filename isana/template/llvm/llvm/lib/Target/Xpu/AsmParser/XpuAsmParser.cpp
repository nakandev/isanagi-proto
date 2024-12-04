//===- {{ namespace }}AsmParser.cpp - Parse {{ namespace }} assembly to MCInst instructions -===//

#include "MCTargetDesc/{{ namespace }}MCTargetDesc.h"
#include "TargetInfo/{{ namespace }}TargetInfo.h"
#include "llvm/ADT/STLExtras.h"
#include "llvm/ADT/StringSwitch.h"
#include "llvm/MC/MCContext.h"
#include "llvm/MC/MCExpr.h"
#include "llvm/MC/MCInst.h"
#include "llvm/MC/MCInstrInfo.h"
#include "llvm/MC/MCParser/MCAsmLexer.h"
#include "llvm/MC/MCParser/MCParsedAsmOperand.h"
#include "llvm/MC/MCParser/MCTargetAsmParser.h"
#include "llvm/MC/MCRegisterInfo.h"
#include "llvm/MC/MCStreamer.h"
#include "llvm/MC/MCSubtargetInfo.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Support/Casting.h"

using namespace llvm;

#define DEBUG_TYPE "{{ namespace.lower() }}-asm-parser"

namespace {
struct {{ namespace }}Operand;

class {{ namespace }}AsmParser : public MCTargetAsmParser {

  SMLoc getLoc() const { return getParser().getTok().getLoc(); }

  bool MatchAndEmitInstruction(SMLoc IDLoc, unsigned &Opcode,
                               OperandVector &Operands, MCStreamer &Out,
                               uint64_t &ErrorInfo,
                               bool MatchingInlineAsm) override;

  // used for .cfi directives
  bool parseRegister(MCRegister &Reo, SMLoc &StartLoc, SMLoc &EndLoc) override;
  ParseStatus tryParseRegister(MCRegister &Reg, SMLoc &StartLoc,
                               SMLoc &EndLoc) override;

  bool ParseInstruction(ParseInstructionInfo &Info, StringRef Name,
                        SMLoc NameLoc, OperandVector &Operands) override;

  // "=" is used as assignment operator for assembly statment, so can't be used
  // for symbol assignment.
  bool equalIsAsmAssignment() override { return false; }
  // "*" is used for dereferencing memory that it will be the start of
  // statement.
  bool starIsStartOfStatement() override { return true; }

#define GET_ASSEMBLER_HEADER
#include "{{ namespace }}GenAsmMatcher.inc"

  ParseStatus parseImmediate(OperandVector &Operands);
  ParseStatus parseMemOpBaseReg(OperandVector &Operands);
  ParseStatus parseRegister(OperandVector &Operands);
  {% for asmopcls in asm_operand_clss -%}
  ParseStatus parse{{ asmopcls.name }}AsmOp(OperandVector &Operands);
  {% endfor -%}
  bool parseOperand(OperandVector &Operands, StringRef Mnemonic);

public:
  enum {{ namespace }}MatchResultTy {
    Match_Dummy = FIRST_TARGET_MATCH_RESULT_TY,
#define GET_OPERAND_DIAGNOSTIC_TYPES
#include "{{ namespace }}GenAsmMatcher.inc"
#undef GET_OPERAND_DIAGNOSTIC_TYPES
  };

  {{ namespace }}AsmParser(const MCSubtargetInfo &STI, MCAsmParser &Parser,
               const MCInstrInfo &MII, const MCTargetOptions &Options)
      : MCTargetAsmParser(Options, STI, MII) {
    MCAsmParserExtension::Initialize(Parser);
    Parser.addAliasForDirective(".half", ".2byte");
    Parser.addAliasForDirective(".hword", ".2byte");
    Parser.addAliasForDirective(".word", ".4byte");
    Parser.addAliasForDirective(".dword", ".8byte");
    setAvailableFeatures(ComputeAvailableFeatures(STI.getFeatureBits()));
  }
};

/// {{ namespace }}Operand - Instances of this class represent a parsed machine
/// instruction
struct {{ namespace }}Operand : public MCParsedAsmOperand {

  enum KindTy {
    Token,
    Register,
    Immediate,
  } Kind;

  struct RegOp {
    unsigned RegNum;
  };

  struct ImmOp {
    const MCExpr *Val;
  };

  SMLoc StartLoc, EndLoc;
  union {
    StringRef Tok;
    RegOp Reg;
    ImmOp Imm;
  };

  {{ namespace }}Operand(KindTy K) : Kind(K) {}

public:
  {{ namespace }}Operand(const {{ namespace }}Operand &o) : MCParsedAsmOperand() {
    Kind = o.Kind;
    StartLoc = o.StartLoc;
    EndLoc = o.EndLoc;

    switch (Kind) {
    case Register:
      Reg = o.Reg;
      break;
    case Immediate:
      Imm = o.Imm;
      break;
    case Token:
      Tok = o.Tok;
      break;
    }
  }

  bool isToken() const override { return Kind == Token; }
  bool isReg() const override { return Kind == Register; }
  bool isImm() const override { return Kind == Immediate; }
  bool isMem() const override { return false; }

  bool isConstantImm() const {
    return isImm() && isa<MCConstantExpr>(getImm());
  }

  int64_t getConstantImm() const {
    const MCExpr *Val = getImm();
    return static_cast<const MCConstantExpr *>(Val)->getValue();
  }

  bool isSImm16() const {
    return (isConstantImm() && isInt<16>(getConstantImm()));
  }

  bool isSymbolRef() const { return isImm() && isa<MCSymbolRefExpr>(getImm()); }

  bool isBrTarget() const { return isSymbolRef() || isSImm16(); }  // TODO fix it

  /// getStartLoc - Gets location of the first token of this operand
  SMLoc getStartLoc() const override { return StartLoc; }
  /// getEndLoc - Gets location of the last token of this operand
  SMLoc getEndLoc() const override { return EndLoc; }

  MCRegister getReg() const override {
    assert(Kind == Register && "Invalid type access!");
    return Reg.RegNum;
  }

  const MCExpr *getImm() const {
    assert(Kind == Immediate && "Invalid type access!");
    return Imm.Val;
  }

  StringRef getToken() const {
    assert(Kind == Token && "Invalid type access!");
    return Tok;
  }

  void print(raw_ostream &OS) const override {
    switch (Kind) {
    case Immediate:
      OS << *getImm();
      break;
    case Register:
      OS << "<register x";
      OS << getReg() << ">";
      break;
    case Token:
      OS << "'" << getToken() << "'";
      break;
    }
  }

  void addExpr(MCInst &Inst, const MCExpr *Expr) const {
    assert(Expr && "Expr shouldn't be null!");

    if (auto *CE = dyn_cast<MCConstantExpr>(Expr))
      Inst.addOperand(MCOperand::createImm(CE->getValue()));
    else
      Inst.addOperand(MCOperand::createExpr(Expr));
  }

  // Used by the TableGen Code
  void addRegOperands(MCInst &Inst, unsigned N) const {
    assert(N == 1 && "Invalid number of operands!");
    Inst.addOperand(MCOperand::createReg(getReg()));
  }

  void addImmOperands(MCInst &Inst, unsigned N) const {
    assert(N == 1 && "Invalid number of operands!");
    addExpr(Inst, getImm());
  }

  static std::unique_ptr<{{ namespace }}Operand> createToken(StringRef Str, SMLoc S) {
    auto Op = std::make_unique<{{ namespace }}Operand>(Token);
    Op->Tok = Str;
    Op->StartLoc = S;
    Op->EndLoc = S;
    return Op;
  }

  static std::unique_ptr<{{ namespace }}Operand> createReg(unsigned RegNo, SMLoc S,
                                               SMLoc E) {
    auto Op = std::make_unique<{{ namespace }}Operand>(Register);
    Op->Reg.RegNum = RegNo;
    Op->StartLoc = S;
    Op->EndLoc = E;
    return Op;
  }

  static std::unique_ptr<{{ namespace }}Operand> createImm(const MCExpr *Val, SMLoc S,
                                               SMLoc E) {
    auto Op = std::make_unique<{{ namespace }}Operand>(Immediate);
    Op->Imm.Val = Val;
    Op->StartLoc = S;
    Op->EndLoc = E;
    return Op;
  }
};
} // end anonymous namespace.

#define GET_REGISTER_MATCHER
#define GET_MATCHER_IMPLEMENTATION
#include "{{ namespace }}GenAsmMatcher.inc"

bool {{ namespace }}AsmParser::MatchAndEmitInstruction(SMLoc IDLoc, unsigned &Opcode,
                                           OperandVector &Operands,
                                           MCStreamer &Out, uint64_t &ErrorInfo,
                                           bool MatchingInlineAsm) {
  MCInst Inst;
  SMLoc ErrorLoc;

  switch (MatchInstructionImpl(Operands, Inst, ErrorInfo, MatchingInlineAsm)) {
  default:
    break;
  case Match_Success:
    Inst.setLoc(IDLoc);
    Out.emitInstruction(Inst, getSTI());
    return false;
  case Match_MissingFeature:
    return Error(IDLoc, "instruction use requires an option to be enabled");
  case Match_MnemonicFail:
    return Error(IDLoc, "unrecognized instruction mnemonic");
  case Match_InvalidOperand:
    ErrorLoc = IDLoc;

    if (ErrorInfo != ~0U) {
      if (ErrorInfo >= Operands.size())
        return Error(ErrorLoc, "too few operands for instruction");

      ErrorLoc = (({{ namespace }}Operand &)*Operands[ErrorInfo]).getStartLoc();

      if (ErrorLoc == SMLoc())
        ErrorLoc = IDLoc;
    }

    return Error(ErrorLoc, "invalid operand for instruction");
  // case Match_InvalidBrTarget:
  //   return Error(Operands[ErrorInfo]->getStartLoc(),
  //                "operand is not an identifier or 16-bit signed integer");
  // case Match_InvalidSImm16:
  //   return Error(Operands[ErrorInfo]->getStartLoc(),
  //                "operand is not a 16-bit signed integer");
  }

  llvm_unreachable("Unknown match type detected!");
}

bool {{ namespace }}AsmParser::parseRegister(MCRegister &Reg, SMLoc &StartLoc,
                                 SMLoc &EndLoc) {
  if (!tryParseRegister(Reg, StartLoc, EndLoc).isSuccess())
    return Error(StartLoc, "invalid register name");
  return false;
}

ParseStatus {{ namespace }}AsmParser::tryParseRegister(MCRegister &Reg, SMLoc &StartLoc,
                                           SMLoc &EndLoc) {
  const AsmToken &Tok = getParser().getTok();
  StartLoc = Tok.getLoc();
  EndLoc = Tok.getEndLoc();
  Reg = {{ namespace }}::NoRegister;
  StringRef Name = getLexer().getTok().getIdentifier();

  if (!MatchRegisterName(Name)) {
    getParser().Lex(); // Eat identifier token.
    return ParseStatus::Success;
  }

  return ParseStatus::NoMatch;
}

ParseStatus {{ namespace }}AsmParser::parseRegister(OperandVector &Operands) {
  SMLoc S = getLoc();
  SMLoc E = SMLoc::getFromPointer(S.getPointer() - 1);

  switch (getLexer().getKind()) {
  default:
    return ParseStatus::NoMatch;
  case AsmToken::Identifier:
    StringRef Name = getLexer().getTok().getIdentifier();
    unsigned RegNo = MatchRegisterName(Name);

    if (RegNo == 0)
      return ParseStatus::NoMatch;

    getLexer().Lex();
    Operands.push_back({{ namespace }}Operand::createReg(RegNo, S, E));
  }
  return ParseStatus::Success;
}

ParseStatus {{ namespace }}AsmParser::parseImmediate(OperandVector &Operands) {
  switch (getLexer().getKind()) {
  default:
    return ParseStatus::NoMatch;
  case AsmToken::LParen:
  case AsmToken::Minus:
  case AsmToken::Plus:
  case AsmToken::Integer:
  case AsmToken::String:
  case AsmToken::Identifier:
    break;
  }

  const MCExpr *IdVal;
  SMLoc S = getLoc();

  if (getParser().parseExpression(IdVal))
    return ParseStatus::Failure;

  SMLoc E = SMLoc::getFromPointer(S.getPointer() - 1);
  Operands.push_back({{ namespace }}Operand::createImm(IdVal, S, E));

  return ParseStatus::Success;
}

ParseStatus {{ namespace }}AsmParser::parseMemOpBaseReg(OperandVector &Operands) {
  if (parseToken(AsmToken::LParen, "expected '('"))
    return ParseStatus::Failure;
  Operands.push_back({{ namespace }}Operand::createToken("(", getLoc()));

  if (!parseRegister(Operands).isSuccess())
    return Error(getLoc(), "expected register");

  if (parseToken(AsmToken::RParen, "expected ')'"))
    return ParseStatus::Failure;
  Operands.push_back({{ namespace }}Operand::createToken(")", getLoc()));

  return ParseStatus::Success;
}

{% for asmopcls in asm_operand_clss -%}
ParseStatus {{ namespace }}AsmParser::parse{{ asmopcls.name }}AsmOp(OperandVector &Operands) {
  SMLoc S = getLoc();
  SMLoc E = SMLoc::getFromPointer(S.getPointer() - 1);

  switch (getLexer().getKind()) {
  default:
    return ParseStatus::NoMatch;
  case AsmToken::Identifier:
    StringRef Name = getLexer().getTok().getIdentifier();
    int64_t ImmVal = StringSwitch<int64_t>(Name)
      {% for k, v in asmopcls.enums.items() -%}
      .Case("{{ v }}", {{ k }})
      {% endfor -%}
      .Default(-1);

    if (ImmVal == -1)
      return ParseStatus::NoMatch;

    getLexer().Lex();
    Operands.push_back({{ namespace }}Operand::createImm(
      MCConstantExpr::create(ImmVal, getContext()), S, E)
    );
    break;
  }
  return ParseStatus::Success;
}
{% endfor %}

bool {{ namespace }}AsmParser::parseOperand(OperandVector &Operands, StringRef Mnemonic) {
  // Check if the current operand has a custom associated parser, if so, try to
  // custom parse the operand, or fallback to the general approach.
{% if asm_operand_clss|length == 0 %}#if 0 // no custom parser{% endif %}
  ParseStatus Result =
      MatchOperandParserImpl(Operands, Mnemonic, /*ParseForAllFeatures=*/true);
  if (Result.isSuccess())
    return false;
  if (Result.isFailure())
    return true;
{% if asm_operand_clss|length == 0 %}#endif{% endif %}

  // Attempt to parse token as a register.
  if (parseRegister(Operands).isSuccess())
    return false;

  // Attempt to parse token as an immediate
  if (parseImmediate(Operands).isSuccess()) {
    // Parse memory base register if present
    if (getLexer().is(AsmToken::LParen))
      return !parseMemOpBaseReg(Operands).isSuccess();
    return false;
  }

  // Finally we have exhausted all options and must declare defeat.
  Error(getLoc(), "unknown operand");
  return true;
}

/// ParseInstruction - Parse an {{ namespace }} instruction which is in {{ namespace }} verifier
/// format. Return true if failure.
bool {{ namespace }}AsmParser::ParseInstruction(ParseInstructionInfo &Info, StringRef Name,
                                    SMLoc NameLoc, OperandVector &Operands) {
  // Parse token as operator nimonic
  Operands.push_back({{ namespace }}Operand::createToken(Name, NameLoc));

  // If there are no more operands, then finish
  if (getLexer().is(AsmToken::EndOfStatement)) {
    getParser().Lex(); // Consume the EndOfStatement.
    return false;
  }

  // Parse first operand
  if (parseOperand(Operands, Name))
    return true;

  // Parse until end of statement, consuming commas between operands
  while (parseOptionalToken(AsmToken::Comma)) {
    // Parse next operand
    if (parseOperand(Operands, Name))
      return true;
  }

  if (getParser().parseEOL("unexpected token")) {
    getParser().eatToEndOfStatement();
    return true;
  }
  return false;
}

extern "C" LLVM_EXTERNAL_VISIBILITY void LLVMInitialize{{ namespace }}AsmParser() {
  RegisterMCAsmParser<{{ namespace }}AsmParser> Z(getThe{{ namespace }}32leTarget());
  RegisterMCAsmParser<{{ namespace }}AsmParser> Y(getThe{{ namespace }}32beTarget());
  RegisterMCAsmParser<{{ namespace }}AsmParser> X(getThe{{ namespace }}64leTarget());
  RegisterMCAsmParser<{{ namespace }}AsmParser> W(getThe{{ namespace }}64beTarget());
}
