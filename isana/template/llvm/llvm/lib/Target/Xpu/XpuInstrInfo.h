//===-- {{ namespace }}InstrInfo.h - {{ namespace }} Instruction Information -*- C++ -*-===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}INSTRINFO_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}INSTRINFO_H

#include "{{ namespace }}RegisterInfo.h"
#include "llvm/CodeGen/TargetInstrInfo.h"

#define GET_INSTRINFO_HEADER
#include "{{ namespace }}GenInstrInfo.inc"

namespace llvm {

class {{ namespace }}Subtarget;

class {{ namespace }}InstrInfo : public {{ namespace }}GenInstrInfo {
public:
  {{ namespace }}InstrInfo();

  bool expandPostRAPseudo(MachineInstr &MI) const override;

  void addImmediate(Register DstReg, Register SrcReg, int64_t Amount,
                    MachineBasicBlock &MBB,
                    MachineBasicBlock::iterator I) const;

  void copyPhysReg(MachineBasicBlock &MBB, MachineBasicBlock::iterator MBBI,
                   const DebugLoc &DL, MCRegister DstReg, MCRegister SrcReg,
                   bool KillSrc, bool RenamableDest = false,
                   bool RenamableSrc = false) const override;

protected:
  const {{ namespace }}Subtarget &STI;

private:
  void expandPseudoRET(MachineBasicBlock &MBB, MachineBasicBlock::iterator I) const;
};
}

#endif
