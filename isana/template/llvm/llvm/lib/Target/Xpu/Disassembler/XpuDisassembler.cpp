//===- {{ namespace }}Disassembler.cpp - Disassembler for {{ namespace }} -===//

// #include "MCTargetDesc/{{ namespace }}BaseInfo.h"
#include "MCTargetDesc/{{ namespace }}MCTargetDesc.h"
#include "TargetInfo/{{ namespace }}TargetInfo.h"
#include "llvm/ADT/DenseMap.h"
#include "llvm/MC/MCContext.h"
#include "llvm/MC/MCDecoderOps.h"
#include "llvm/MC/MCDisassembler/MCDisassembler.h"
#include "llvm/MC/MCInst.h"
#include "llvm/MC/MCInstrInfo.h"
#include "llvm/MC/MCRegisterInfo.h"
#include "llvm/MC/MCSubtargetInfo.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Support/Endian.h"

using namespace llvm;

#define DEBUG_TYPE "{{ namespace.lower() }}-disassembler"

typedef MCDisassembler::DecodeStatus DecodeStatus;

namespace {
class {{ namespace }}Disassembler : public MCDisassembler {
  std::unique_ptr<MCInstrInfo const> const MCII;
  mutable StringRef symbolName;

public:
  {{ namespace }}Disassembler(const MCSubtargetInfo &STI, MCContext &Ctx,
                   MCInstrInfo const *MCII);

  DecodeStatus getInstruction(MCInst &Instr, uint64_t &Size,
                              ArrayRef<uint8_t> Bytes, uint64_t Address,
                              raw_ostream &CStream) const override;
};
} // end anonymous namespace

{{ namespace }}Disassembler::{{ namespace }}Disassembler(const MCSubtargetInfo &STI, MCContext &Ctx,
                                   MCInstrInfo const *MCII)
    : MCDisassembler(STI, Ctx), MCII(MCII) {}

static MCDisassembler *create{{ namespace }}Disassembler(const Target &T,
                                              const MCSubtargetInfo &STI,
                                              MCContext &Ctx) {
  return new {{ namespace }}Disassembler(STI, Ctx, T.createMCInstrInfo());
}

extern "C" LLVM_EXTERNAL_VISIBILITY void LLVMInitialize{{ namespace }}Disassembler() {
  TargetRegistry::RegisterMCDisassembler(getThe{{ namespace }}32leTarget(),
                                         create{{ namespace }}Disassembler);
}

{#
{% for regcls in regcls_defs -%}
static const uint16_t DecoderTable{{ regcls.varname }}[] = {
{{ regcls.reg_varnames }}
};
{% endfor %}
#}

{% for regcls in regcls_defs -%}
static DecodeStatus Decode{{ regcls.varname }}RegisterClass(MCInst &Inst, uint64_t RegNo,
                                           uint64_t Address,
                                           const MCDisassembler *Decoder) {
  // if (RegNo >= {{ regcls.regs|length }})
  //   return MCDisassembler::Fail;
  // 
  // Inst.addOperand(MCOperand::createReg(DecoderTable{{ regcls.varname }}[RegNo]));
  uint16_t RegVar;
  switch (RegNo) {
  default:
    return MCDisassembler::Fail;
  {% for reg in regcls.regs -%}
  case {{ reg.number }}: RegVar = {{ namespace }}::{{ reg.label.upper() }}; break;
  {% endfor %}
  }
  Inst.addOperand(MCOperand::createReg(RegVar));
  return MCDisassembler::Success;
}
{% endfor %}

template <unsigned N, unsigned S>
static DecodeStatus decodeUImmOperand(MCInst &Inst, uint64_t Imm,
                                      int64_t Address,
                                      const MCDisassembler *Decoder) {
  assert(isUInt<N>(Imm) && "Invalid immediate");
  Inst.addOperand(MCOperand::createImm(Imm << S));
  return MCDisassembler::Success;
}

template <unsigned N, unsigned S>
static DecodeStatus decodeSImmOperand(MCInst &Inst, uint64_t Imm,
                                      int64_t Address,
                                      const MCDisassembler *Decoder) {
  assert(isUInt<N>(Imm) && "Invalid immediate");
  // Sign-extend the number in the bottom N bits of Imm
  Inst.addOperand(MCOperand::createImm(SignExtend64<N>(Imm) << S));
  return MCDisassembler::Success;
}

static DecodeStatus decodeImmShiftOpValue(MCInst &Inst, uint64_t Imm,
                                          int64_t Address,
                                          const MCDisassembler *Decoder) {
  Inst.addOperand(MCOperand::createImm(Log2_64(Imm)));
  return MCDisassembler::Success;
}

#include "{{ namespace }}GenDisassemblerTables.inc"

DecodeStatus {{ namespace }}Disassembler::getInstruction(MCInst &MI, uint64_t &Size,
                                              ArrayRef<uint8_t> Bytes,
                                              uint64_t Address,
                                              raw_ostream &CS) const {

  uint32_t Insn;
  DecodeStatus Result = MCDisassembler::Fail;

  if (Bytes.size() < 2) {
    Size = 0;
    return MCDisassembler::Fail;
  }

  {% if 16 in instr_bitsizes -%}
  Insn = support::endian::read16le(Bytes.data());
  LLVM_DEBUG(dbgs() << "Trying {{ namespace }} 16-bit table :\n");
  Result = decodeInstruction(DecoderTable{{ namespace }}16, MI, Insn, Address, this, STI);
  if (Result != MCDisassembler::Fail) {
    Size = 2;
    return Result;
  }
  {%- endif %}
  {%- if 32 in instr_bitsizes -%}
  Insn = support::endian::read32le(Bytes.data());
  LLVM_DEBUG(dbgs() << "Trying {{ namespace }} 32-bit table :\n");
  Result = decodeInstruction(DecoderTable{{ namespace }}32, MI, Insn, Address, this, STI);
  if (Result != MCDisassembler::Fail) {
    Size = 4;
    return Result;
  }
  {%- endif %}
  {%- if 64 in instr_bitsizes -%}
  Insn = support::endian::read32le(Bytes.data());
  LLVM_DEBUG(dbgs() << "Trying {{ namespace }} 64-bit table :\n");
  Result = decodeInstruction(DecoderTable{{ namespace }}64, MI, Insn, Address, this, STI);
  if (Result != MCDisassembler::Fail) {
    Size = 8;
    return Result;
  }
  {%- endif %}
  return Result;
}