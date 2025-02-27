//===-- {{ Xpu }}FrameLowering.h - Define frame lowering for {{ Xpu }} -*- C++ -*--===//

#ifndef LLVM_LIB_TARGET_{{ XPU }}_{{ XPU }}FRAMELOWERING_H
#define LLVM_LIB_TARGET_{{ XPU }}_{{ XPU }}FRAMELOWERING_H

#include "llvm/CodeGen/TargetFrameLowering.h"

namespace llvm {
class {{ Xpu }}Subtarget;

class {{ Xpu }}FrameLowering : public TargetFrameLowering {
public:
  explicit {{ Xpu }}FrameLowering(const {{ Xpu }}Subtarget &STI)
      : TargetFrameLowering(StackGrowsDown, Align(8), 0), STI(STI) {}

  void emitPrologue(MachineFunction &MF, MachineBasicBlock &MBB) const override;
  void emitEpilogue(MachineFunction &MF, MachineBasicBlock &MBB) const override;

  bool hasFP(const MachineFunction &MF) const override;
  void determineCalleeSaves(MachineFunction &MF, BitVector &SavedRegs,
                            RegScavenger *RS) const override;

  MachineBasicBlock::iterator
  eliminateCallFramePseudoInstr(MachineFunction &MF, MachineBasicBlock &MBB,
                                MachineBasicBlock::iterator MI) const override;

protected:
  const {{ Xpu }}Subtarget &STI;
};
}
#endif
