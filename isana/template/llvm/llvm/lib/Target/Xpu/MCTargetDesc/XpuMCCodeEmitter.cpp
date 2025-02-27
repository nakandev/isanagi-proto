//===- {{ namespace }}MCCodeEmitter.cpp - Convert {{ namespace }} code to machine code -===//

#include "MCTargetDesc/{{ namespace }}FixupKinds.h"
#include "MCTargetDesc/{{ namespace }}MCExpr.h"
#include "MCTargetDesc/{{ namespace }}MCTargetDesc.h"
#include "llvm/ADT/SmallVector.h"
#include "llvm/MC/MCCodeEmitter.h"
#include "llvm/MC/MCContext.h"
#include "llvm/MC/MCExpr.h"
#include "llvm/MC/MCFixup.h"
#include "llvm/MC/MCInst.h"
#include "llvm/MC/MCInstBuilder.h"
#include "llvm/MC/MCInstrInfo.h"
#include "llvm/MC/MCRegisterInfo.h"
#include "llvm/MC/MCSubtargetInfo.h"
#include "llvm/Support/Casting.h"
#include "llvm/Support/Endian.h"
#include "llvm/Support/EndianStream.h"

using namespace llvm;

#define DEBUG_TYPE "mccodeemitter"

namespace {

class {{ namespace }}MCCodeEmitter : public MCCodeEmitter {
  const MCInstrInfo &MCII;
  const MCRegisterInfo &MRI;
  bool IsBigEndian;
  bool Is64Bit;

public:
  {{ namespace }}MCCodeEmitter(const MCInstrInfo &mcii, const MCRegisterInfo &mri,
                   bool IsBigEndian, bool Is64Bit)
      : MCII(mcii), MRI(mri), IsBigEndian(IsBigEndian), Is64Bit(Is64Bit) { }
  {{ namespace }}MCCodeEmitter(const {{ namespace }}MCCodeEmitter &) = delete;
  void operator=(const {{ namespace }}MCCodeEmitter &) = delete;
  ~{{ namespace }}MCCodeEmitter() override = default;

  // getBinaryCodeForInstr - TableGen'erated function for getting the
  // binary encoding for an instruction.
  uint64_t getBinaryCodeForInstr(const MCInst &MI,
      SmallVectorImpl<MCFixup> &Fixups,
      const MCSubtargetInfo &STI) const;

  // getMachineOpValue - Return binary encoding of operand. If the machin
  // operand requires relocation, record the relocation and return zero.
  unsigned getMachineOpValue(const MCInst &MI, const MCOperand &MO,
    SmallVectorImpl<MCFixup> &Fixups,
    const MCSubtargetInfo &STI) const;

  template <unsigned S>
  unsigned getImmOpValueRShift(
    const MCInst &MI, unsigned OpNo,
    SmallVectorImpl<MCFixup> &Fixups,
    const MCSubtargetInfo &STI) const;

  // uint64_t getMemoryOpValue(const MCInst &MI, unsigned Op,
  //   SmallVectorImpl<MCFixup> &Fixups,
  //   const MCSubtargetInfo &STI) const;

  void encodeInstruction(const MCInst &MI, SmallVectorImpl<char> &CB,
    SmallVectorImpl<MCFixup> &Fixups,
    const MCSubtargetInfo &STI) const override;

  void expandFunctionCall(const MCInst &MI, SmallVectorImpl<char> &CB,
                          SmallVectorImpl<MCFixup> &Fixups,
                          const MCSubtargetInfo &STI) const;
};

} // end anonymous namespace

MCCodeEmitter *
llvm::create{{ namespace }}MCCodeEmitter(
  const MCInstrInfo &MCII,
  MCContext &Ctx
)
{
  return new {{ namespace }}MCCodeEmitter(MCII, *Ctx.getRegisterInfo(), false, false);
}

void
{{ namespace }}MCCodeEmitter::expandFunctionCall(
  const MCInst &MI,
  SmallVectorImpl<char> &CB,
  SmallVectorImpl<MCFixup> &Fixups,
  const MCSubtargetInfo &STI
) const {
  MCInst TmpInst;
  MCOperand Func;
  MCRegister Ra;
  uint32_t Binary;

  if (MI.getOpcode() == {{ namespace }}::PseudoCALL) {
    Func = MI.getOperand(0);
    Ra = {{ namespace }}::X1;
  }

  assert(Func.isExpr() && "Expected expression");

  const MCExpr *CallExpr = Func.getExpr();

#if 0
  // long jump
  //  auipc x1, $func | auipc x1, 0
  //                  |   + fixup:pc_rel
  //  jalr x1, x1, 0  | jalr x1, x1, 0
  TmpInst = MCInstBuilder({{ namespace }}::AUIPC).addReg(Ra).addExpr(CallExpr);
  Binary = getBinaryCodeForInstr(TmpInst, Fixups, STI);
  support::endian::write(CB, Binary, llvm::endianness::little);

  TmpInst = MCInstBuilder({{ namespace }}::JALR).addReg(Ra).addReg(Ra).addImm(0);
  Binary = getBinaryCodeForInstr(TmpInst, Fixups, STI);
  support::endian::write(CB, Binary, llvm::endianness::little);
#endif
  // short jump
  // jal x1, $func    | jal x1, 0
  //                  |   + fixup:pc_rel
  TmpInst = MCInstBuilder({{ namespace }}::JAL).addReg(Ra).addExpr(CallExpr);
  Binary = getBinaryCodeForInstr(TmpInst, Fixups, STI);
  support::endian::write(CB, Binary, llvm::endianness::little);
}

unsigned
{{ namespace }}MCCodeEmitter::getMachineOpValue(
  const MCInst &MI,
  const MCOperand &MO,
  SmallVectorImpl<MCFixup> &Fixups,
  const MCSubtargetInfo &STI
) const
{
  if (MO.isReg())
    return MRI.getEncodingValue(MO.getReg());
  if (MO.isImm())
    return static_cast<unsigned>(MO.getImm());

  // llvm_unreachable("Unhandled expression!");
  const MCExpr *Expr = MO.getExpr();
  MCExpr::ExprKind Kind = Expr->getKind();
  {{ namespace }}::Fixups FixupKind = {{ namespace }}::fixup_{{ namespace.lower() }}_invalid;
  if (Kind == MCExpr::Target) {
    const {{ namespace }}MCExpr *XExpr = cast<{{ namespace }}MCExpr>(Expr);
    switch (XExpr->getKind()) {
    default:
      break;
    case {{ namespace }}MCExpr::VK_{{ namespace }}_None:
    case {{ namespace }}MCExpr::VK_{{ namespace }}_Invalid:
      llvm_unreachable("Unhandled fixup kind!");
    case {{ namespace }}MCExpr::VK_{{ namespace }}_CALL:
          FixupKind = {{ namespace }}::fixup_{{ namespace.lower() }}_pc_rel_1;  // TODO fix it
    case {{ namespace }}MCExpr::VK_{{ namespace }}_SYMBOL:
      // FixupKind = {{ namespace }}::fixup_{{ namespace.lower() }}_other_imm_0;  // TODO this is trial.
      {
        unsigned Opcode = MI.getOpcode();
        switch (Opcode) {
        default:
          break;
        {% for fx in fixup_relocs -%}
        {% for instr in fx.instrs -%}
        case {{ namespace }}::{{ instr.__class__.__name__.upper() }}:
        {% endfor %}  FixupKind = {{ namespace }}::{{ fx.name_enum}};
          break;
        {% endfor -%}
        }
      }
      break;
    }
  } else if ((Kind == MCExpr::SymbolRef &&
                 cast<MCSymbolRefExpr>(Expr)->getKind() ==
                     MCSymbolRefExpr::VK_None) ||
             Kind == MCExpr::Binary) {
      unsigned Opcode = MI.getOpcode();
      switch (Opcode) {
      default:
        break;
      {% for fx in fixup_relocs -%}
      {% for instr in fx.instrs -%}
      case {{ namespace }}::{{ instr.__class__.__name__.upper() }}:
      {% endfor %}  FixupKind = {{ namespace }}::{{ fx.name_enum}};
        break;
      {% endfor -%}
      }
  }

  assert(FixupKind != {{ namespace }}::fixup_{{ namespace.lower() }}_invalid && "Unhandled expression!");

  Fixups.push_back(
      MCFixup::create(0, Expr, MCFixupKind(FixupKind), MI.getLoc()));
  return 0;
}

template <unsigned S>
unsigned
{{ namespace }}MCCodeEmitter::getImmOpValueRShift(
  const MCInst &MI, unsigned OpNo,
  SmallVectorImpl<MCFixup> &Fixups,
  const MCSubtargetInfo &STI
) const {
  const MCOperand &MO = MI.getOperand(OpNo);

  if (MO.isImm()) {
    unsigned Res = MO.getImm();
    assert((Res & ((1 << S) - 1)) == 0 && "LSB is non-zero");
    return Res >> S;
  }
  return getMachineOpValue (MI, MO, Fixups, STI);
}

void
{{ namespace }}MCCodeEmitter::encodeInstruction(
  const MCInst &MI,
  SmallVectorImpl<char> &CB,
  SmallVectorImpl<MCFixup> &Fixups,
  const MCSubtargetInfo &STI
) const
{
  const unsigned Opcode = MI.getOpcode();
  const MCInstrDesc &Desc = MCII.get(Opcode);
  unsigned Size = Desc.getSize();

  switch (MI.getOpcode()) {
  default:
    break;
  case CustomXPU::PseudoCALL:
    expandFunctionCall(MI, CB, Fixups, STI);
    return;
  }

  // Get instruction encoding and emit it
  auto Endian = IsBigEndian ? llvm::endianness::big : llvm::endianness::little;
  switch (Size) {
  case 2: {
    uint16_t Binary = getBinaryCodeForInstr(MI, Fixups, STI);
    support::endian::write<uint16_t>(CB, Binary, Endian);
    break;
  }
  case 4: {
    uint32_t Binary = getBinaryCodeForInstr(MI, Fixups, STI);
    support::endian::write<uint32_t>(CB, Binary, Endian);
    break;
  }
  case 8: {
    uint64_t Binary = getBinaryCodeForInstr(MI, Fixups, STI);
    support::endian::write<uint64_t>(CB, Binary, Endian);
    break;
  }
  default: {
    llvm_unreachable("Unhandled encodeInstruction length!");
  }
  }
}

#include "{{ namespace }}GenMCCodeEmitter.inc"
