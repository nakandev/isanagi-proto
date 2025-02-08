//===-- {{ namespace }}InstrInfo.h - {{ namespace }} Instruction Information -*- C++ -*-===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}INSTRINFO_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}INSTRINFO_H

#include "{{ namespace }}RegisterInfo.h"
#include "llvm/CodeGen/TargetInstrInfo.h"

#define GET_INSTRINFO_HEADER
#include "{{ namespace }}GenInstrInfo.inc"

namespace llvm {

class {{ namespace }}InstrInfo : public {{ namespace }}GenInstrInfo {
public:
  {{ namespace }}InstrInfo();

  bool expandPostRAPseudo(MachineInstr &MI) const override;

  void addImmediate(Register DstReg, Register SrcReg, int64_t Amount,
                    MachineBasicBlock &MBB,
                    MachineBasicBlock::iterator I) const;

private:
  void expandPseudoRET(MachineBasicBlock &MBB, MachineBasicBlock::iterator I) const;
};
}

#endif
