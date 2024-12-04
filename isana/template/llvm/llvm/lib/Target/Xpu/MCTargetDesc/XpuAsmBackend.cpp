//===- {{ namespace }}AsmBackend.cpp - {{ namespace }} Assembler Backend -===//

#include "{{ namespace }}AsmBackend.h"
#include "MCTargetDesc/{{ namespace }}MCTargetDesc.h"
#include "llvm/ADT/DenseMap.h"
#include "llvm/MC/MCAssembler.h"
#include "llvm/MC/MCContext.h"
#include "llvm/MC/MCFixupKindInfo.h"
#include "llvm/MC/MCObjectWriter.h"
// #include "llvm/MC/MCSymbol.h"
#include "llvm/MC/MCValue.h"
#include "llvm/Support/Debug.h"

#define DEBUG_TYPE "{{ namespace.lower() }}-asmbackend"

using namespace llvm;

std::unique_ptr<MCObjectTargetWriter>
{{ namespace }}AsmBackend::createObjectTargetWriter(
) const
{
  return create{{ namespace }}ELFObjectWriter();
}

const MCFixupKindInfo &
{{ namespace }}AsmBackend::getFixupKindInfo(
  MCFixupKind Kind
) const
{
  static llvm::DenseMap<unsigned, MCFixupKindInfo> Infos = {
      {% for fx in fixups -%}
      { {{ namespace }}::Fixups::{{ fx.name_enum }}, {"{{ fx.name_enum }}", {{ fx.offset }}, {{ fx.size }}, {{ fx.flags }}} },
      {% endfor %}
  };

  assert(Infos.size() == {{ namespace }}::NumTargetFixupKinds &&
         "Not all fixup kinds added to Infos array");

  if (FirstTargetFixupKind <= Kind && Kind < FirstLiteralRelocationKind) {
    assert(unsigned(Kind - FirstTargetFixupKind) < getNumFixupKinds() &&
           "Invalid kind!");

    return Infos[Kind];
  } else if (Kind < FirstTargetFixupKind) {
    return MCAsmBackend::getFixupKindInfo(Kind);
  } else {
    return MCAsmBackend::getFixupKindInfo(FK_NONE);
  }
}

static uint64_t
adjustFixupValue(
  const MCFixup &Fixup, uint64_t Value,
  MCContext &Ctx
)
{
  switch (Fixup.getTargetKind()) {
  default:
    llvm_unreachable("Unknown fixup kind!");
  case FK_Data_1:
  case FK_Data_2:
  case FK_Data_4:
  case FK_Data_8:
    return Value;
  {% for fx in fixups_should_force_reloc -%}
  case {{ namespace }}::{{ fx.name_enum }}:
    llvm_unreachable("Relocation should be unconditionally forced\n");
  {% endfor %}
  {% for fx in fixups_adjust -%}
  case {{ namespace }}::{{ fx.name_enum }}: {
    const uint64_t val = Value;  // TODO: remove unused variable
    return 0
    {% for proc in fx.reloc_procs -%}
    {{ proc }}
    {% endfor -%}
    ;
    break;
  }
  {% endfor %}
  }
}

bool
{{ namespace }}AsmBackend::fixupNeedsRelaxationAdvanced(
  const MCAssembler &Asm,
  const MCFixup &Fixup,
  bool Resolved, uint64_t Value,
  const MCRelaxableFragment *DF,
  const bool WasForced
) const
{
  if (!Resolved && !WasForced)
    return true;

  // int64_t Offset = int64_t(Value);
  switch (Fixup.getTargetKind()) {
  default:
    break;
  // case {{ namespace }}::fixup_xxx:
  //   return is_out_of_range(Value);
  }
  return false;
}

void
{{ namespace }}AsmBackend::applyFixup(
  const MCAssembler &Asm, const MCFixup &Fixup,
  const MCValue &Target,
  MutableArrayRef<char> Data, uint64_t Value,
  bool IsResolved,
  const MCSubtargetInfo *STI
) const
{
  MCFixupKind Kind = Fixup.getKind();
  if (Kind >= FirstLiteralRelocationKind)
    return;
  MCContext &Ctx = Asm.getContext();
  MCFixupKindInfo Info = getFixupKindInfo(Kind);
  if (!Value)
    return;

  Value = adjustFixupValue(Fixup, Value, Ctx);
  Value <<= Info.TargetOffset;

  unsigned Offset = Fixup.getOffset();
  unsigned NumBytes = alignTo(Info.TargetSize + Info.TargetOffset, 8) / 8;

  assert(Offset + NumBytes <= Data.size() && "Invalid fixup offset!");

  bool IsLittleEndian = (Endian == llvm::endianness::little);
  // bool IsInstFixup = (Kind >= FirstTargetFixupKind);
  // 
  // if (IsLittleEndian && IsInstFixup && (NumBytes == 4)) {
  //   Data[Offset + 0] |= uint8_t((Value >> 16) & 0xff);
  //   Data[Offset + 1] |= uint8_t((Value >> 24) & 0xff);
  //   Data[Offset + 2] |= uint8_t(Value & 0xff);
  //   Data[Offset + 3] |= uint8_t((Value >> 8) & 0xff);
  // } else {
    for (unsigned I = 0; I != NumBytes; I++) {
      unsigned Idx = IsLittleEndian ? I : (NumBytes - 1 - I);
      Data[Offset + Idx] |= uint8_t((Value >> (I * 8)) & 0xff);
    }
  // }
}

bool
{{ namespace }}AsmBackend::mayNeedRelaxation(
  const MCInst &Inst,
  const MCSubtargetInfo &STI
) const
{
  switch (Inst.getOpcode()) {
  default:
    return false;
  {% for r_instr in relax_instrs -%}
  // case {{ namespace }}::{{ r_instr.opc_enum }}:
  //   return true;
  {% endfor %}
  }
}

bool
{{ namespace }}AsmBackend::shouldForceRelocation(
  const MCAssembler &Asm,
  const MCFixup &Fixup,
  const MCValue &Target,
  const MCSubtargetInfo * /*STI*/
)
{
  if (Fixup.getKind() >= FirstLiteralRelocationKind)
    return true;
  switch (Fixup.getTargetKind()) {
  default:
    break;
  case FK_Data_1:
  case FK_Data_2:
  case FK_Data_4:
  case FK_Data_8:
  case FK_Data_leb128:
    if (Target.isAbsolute())
      return false;
    break;
  {% for fx in fixups_should_force_reloc -%}
  case {{ namespace }}::{{ fx.name_enum }}:
    return true;
  {% endfor -%}
  }

  return false;
}

bool
{{ namespace }}AsmBackend::fixupNeedsRelaxation(
  const MCFixup &Fixup,
  uint64_t Value
) const
{
  return false;
}

void
{{ namespace }}AsmBackend::relaxInstruction(
  MCInst &Inst,
  const MCSubtargetInfo &STI
) const
{
  MCInst Res;

  switch (Inst.getOpcode()) {
  default:
    LLVM_DEBUG(Inst.dump());
    llvm_unreachable("Opcode not expected!");
  {% for r_instr in relax_instrs -%}
  case {{ namespace }}::{{ r_instr.opc_enum }}:
  //   Res.setOpcode({{ namespace }}::{{ r_instr.opc_enum }});
  //   Res.addOperand(Inst.getOperand(0));
  //   Res.addOperand(Inst.getOperand(1));
    break;
  {% endfor -%}
  }
  Inst = std::move(Res);
}

bool
{{ namespace }}AsmBackend::writeNopData(
  raw_ostream &OS, uint64_t Count,
  const MCSubtargetInfo *STI
) const
{
  OS.write_zeros(Count);
  return true;
}

MCAsmBackend *
llvm::create{{ namespace }}AsmBackend(
  const Target &T,
  const MCSubtargetInfo &STI,
  const MCRegisterInfo &MRI,
  const MCTargetOptions &Options
)
{
  return new {{ namespace }}AsmBackend(STI, Options);
}