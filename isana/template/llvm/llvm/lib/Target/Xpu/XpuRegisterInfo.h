//===-- {{ namespace }}RegisterInfo.h - {{ namespace }} Register Information Impl -*- C++ -*-===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}REGISTERINFO_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}REGISTERINFO_H

#include "llvm/CodeGen/TargetRegisterInfo.h"

#define GET_REGINFO_HEADER
#include "{{ namespace }}GenRegisterInfo.inc"

namespace llvm {

struct {{ namespace }}RegisterInfo : public {{ namespace }}GenRegisterInfo {

  {{ namespace }}RegisterInfo();

  const MCPhysReg *getCalleeSavedRegs(const MachineFunction *MF) const override;

  const uint32_t *getCallPreservedMask(const MachineFunction &MF,
                                       CallingConv::ID) const override;

  BitVector getReservedRegs(const MachineFunction &MF) const override;

  bool eliminateFrameIndex(MachineBasicBlock::iterator MI, int SPAdj,
                           unsigned FIOperandNum,
                           RegScavenger *RS = nullptr) const override;

  Register getFrameRegister(const MachineFunction &MF) const override;
};
} // namespace llvm

#endif
