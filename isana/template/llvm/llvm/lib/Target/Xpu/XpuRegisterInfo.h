//===-- {{ Xpu }}RegisterInfo.h - {{ Xpu }} Register Information Impl -*- C++ -*-===//

#ifndef LLVM_LIB_TARGET_{{ XPU }}_{{ XPU }}REGISTERINFO_H
#define LLVM_LIB_TARGET_{{ XPU }}_{{ XPU }}REGISTERINFO_H

#include "llvm/CodeGen/TargetRegisterInfo.h"

#define GET_REGINFO_HEADER
#include "{{ Xpu }}GenRegisterInfo.inc"

namespace llvm {

struct {{ Xpu }}RegisterInfo : public {{ Xpu }}GenRegisterInfo {

  {{ Xpu }}RegisterInfo();

  const MCPhysReg *getCalleeSavedRegs(const MachineFunction *MF) const override;

  const uint32_t *getCallPreservedMask(const MachineFunction &MF,
                                       CallingConv::ID) const override;

  BitVector getReservedRegs(const MachineFunction &MF) const override;

  bool eliminateFrameIndex(MachineBasicBlock::iterator MBBI, int SPAdj,
                           unsigned FIOperandNum,
                           RegScavenger *RS = nullptr) const override;

  Register getFrameRegister(const MachineFunction &MF) const override;

  bool requiresRegisterScavenging(const MachineFunction &MF) const override {
    return true;
  }

  bool requiresFrameIndexScavenging(const MachineFunction &MF) const override {
    return true;
  }
};
} // namespace llvm

#endif
