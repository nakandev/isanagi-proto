//===-- {{ namespace }}AsmPrinter.cpp - {{ namespace }} LLVM assembly writer --===//

#include "{{ namespace }}.h"
#include "{{ namespace }}InstrInfo.h"
#include "{{ namespace }}TargetMachine.h"
#include "MCTargetDesc/{{ namespace }}BaseInfo.h"
#include "MCTargetDesc/{{ namespace }}InstPrinter.h"
#include "MCTargetDesc/{{ namespace }}MCExpr.h"
// #include "MCTargetDesc/{{ namespace }}TargetStreamer.h"
#include "TargetInfo/{{ namespace }}TargetInfo.h"
#include "llvm/CodeGen/AsmPrinter.h"
#include "llvm/CodeGen/MachineConstantPool.h"
#include "llvm/CodeGen/MachineFunctionPass.h"
#include "llvm/CodeGen/MachineInstr.h"
#include "llvm/CodeGen/MachineModuleInfo.h"
#include "llvm/IR/Module.h"
#include "llvm/MC/MCAsmInfo.h"
#include "llvm/MC/MCInst.h"
#include "llvm/MC/MCStreamer.h"
#include "llvm/MC/MCSymbol.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

#define DEBUG_TYPE "asm-printer"

namespace {
class {{ namespace }}AsmPrinter : public AsmPrinter {
public:
  explicit {{ namespace }}AsmPrinter(TargetMachine &TM,
                         std::unique_ptr<MCStreamer> Streamer)
      : AsmPrinter(TM, std::move(Streamer)) {}

  StringRef getPassName() const override { return "{{ namespace }} Assembly Printer"; }
  // bool doInitialization(Module &M) override;
  // bool doFinalization(Module &M) override;

  // bool runOnMachineFunction(MachineFunction &MF) override;

  void emitInstruction(const MachineInstr *MI) override;

  // bool PrintAsmOperand(const MachineInstr *MI, unsigned OpNo,
  //                      const char *ExtraCode, raw_ostream &O) override;
  // bool PrintAsmMemoryOperand(const MachineInstr *MI, unsigned OpNum,
  //                            const char *ExtraCode, raw_ostream &O) override;

  // void emitStartOfAsmFile(Module &M) override;
  // void emitEndOfAsmFile(Module &M) override;

  // void emitFunctionEntryLabel() override;

  bool lowerPseudoInstExpansion(const MachineInstr *MI, MCInst &Inst);
  bool lowerOperand(const MachineOperand &MO, MCOperand &MCOp) const;
  bool lowerToMCInst(const MachineInstr *MI, MCInst &OutMI);
};
} // namespace

// Simple pseudo-instructions have their lowering (with expansion to real
// instructions) auto-generated.
#include "{{ namespace }}GenMCPseudoLowering.inc"

void {{ namespace }}AsmPrinter::emitInstruction(const MachineInstr *MI) {
  {{ namespace }}_MC::verifyInstructionPredicates(MI->getOpcode(),
                                      getSubtargetInfo().getFeatureBits());

  // Do any auto-generated pseudo lowerings.
  if (MCInst OutInst; lowerPseudoInstExpansion(MI, OutInst)) {
    EmitToStreamer(*OutStreamer, OutInst);
    return;
  }

  MCInst OutInst;
  if (!lowerToMCInst(MI, OutInst))
    EmitToStreamer(*OutStreamer, OutInst);
}

static MCOperand lowerSymbolOperand(const MachineOperand &MO, MCSymbol *Sym,
                                    const AsmPrinter &AP) {
  MCContext &Ctx = AP.OutContext;
  {{ namespace }}MCExpr::VariantKind Kind;

  switch(MO.getTargetFlags()) {
  default:
    llvm_unreachable("Unknown target flag on GV operand");
  case {{ namespace }}II::MO_None:
    Kind = {{ namespace }}MCExpr::VK_{{ namespace }}_None;
    break;
  case {{ namespace }}II::MO_CALL:
    Kind = {{ namespace }}MCExpr::VK_{{ namespace }}_CALL;
    break;
  // case {{ namespace }}II::MO_SYMBOL:
  //   Kind = {{ namespace }}MCExpr::VK_{{ namespace }}_SYMBOL;
  //   break;
  }

  const MCExpr *ME =
      MCSymbolRefExpr::create(Sym, MCSymbolRefExpr::VK_None, Ctx);

  if (!MO.isJTI() && !MO.isMBB() && MO.getOffset())
    ME = MCBinaryExpr::createAdd(
        ME, MCConstantExpr::create(MO.getOffset(), Ctx), Ctx);

  if (Kind != {{ namespace }}MCExpr::VK_{{ namespace }}_None)
    ME = {{ namespace }}MCExpr::create(ME, Kind, Ctx);
  return MCOperand::createExpr(ME);
}

bool {{ namespace }}AsmPrinter::lowerOperand(const MachineOperand &MO,
                                   MCOperand &MCOp) const {
  switch (MO.getType()) {
  default:
    report_fatal_error("lowerOperand: unknown operand type");
  case MachineOperand::MO_Register:
    // Ignore all implicit register operands.
    if (MO.isImplicit())
      return false;
    MCOp = MCOperand::createReg(MO.getReg());
    break;
  case MachineOperand::MO_RegisterMask:
    // Regmasks are like implicit defs.
    return false;
  case MachineOperand::MO_Immediate:
    MCOp = MCOperand::createImm(MO.getImm());
    break;
  case MachineOperand::MO_MachineBasicBlock:
    MCOp = lowerSymbolOperand(MO, MO.getMBB()->getSymbol(), *this);
    break;
  case MachineOperand::MO_GlobalAddress:
    MCOp = lowerSymbolOperand(MO, getSymbolPreferLocal(*MO.getGlobal()), *this);
    break;
  case MachineOperand::MO_BlockAddress:
    MCOp = lowerSymbolOperand(MO, GetBlockAddressSymbol(MO.getBlockAddress()),
                              *this);
    break;
  case MachineOperand::MO_ExternalSymbol:
    MCOp = lowerSymbolOperand(MO, GetExternalSymbolSymbol(MO.getSymbolName()),
                              *this);
    break;
  case MachineOperand::MO_ConstantPoolIndex:
    MCOp = lowerSymbolOperand(MO, GetCPISymbol(MO.getIndex()), *this);
    break;
  case MachineOperand::MO_JumpTableIndex:
    MCOp = lowerSymbolOperand(MO, GetJTISymbol(MO.getIndex()), *this);
    break;
  case MachineOperand::MO_MCSymbol:
    MCOp = lowerSymbolOperand(MO, MO.getMCSymbol(), *this);
    break;
  }
  return true;
}

bool {{ namespace }}AsmPrinter::lowerToMCInst(const MachineInstr *MI, MCInst &OutMI) {
  OutMI.setOpcode(MI->getOpcode());

  for (const MachineOperand &MO : MI->operands()) {
    MCOperand MCOp;
    if (lowerOperand(MO, MCOp))
      OutMI.addOperand(MCOp);
  }

  return false;
}

// Force static initialization.
extern "C" LLVM_EXTERNAL_VISIBILITY void LLVMInitialize{{ namespace }}AsmPrinter() {
  RegisterAsmPrinter<{{ namespace }}AsmPrinter> Z(getThe{{ namespace }}32leTarget());
  RegisterAsmPrinter<{{ namespace }}AsmPrinter> Y(getThe{{ namespace }}32beTarget());
  RegisterAsmPrinter<{{ namespace }}AsmPrinter> X(getThe{{ namespace }}64leTarget());
  RegisterAsmPrinter<{{ namespace }}AsmPrinter> W(getThe{{ namespace }}64beTarget());
}
