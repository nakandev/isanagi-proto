//===-- {{ namespace }}FrameLowering.h - Define frame lowering for {{ namespace }} -*- C++ -*--===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}FRAMELOWERING_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}FRAMELOWERING_H

#include "llvm/CodeGen/TargetFrameLowering.h"

namespace llvm {
class {{ namespace }}Subtarget;

class {{ namespace }}FrameLowering : public TargetFrameLowering {
public:
  explicit {{ namespace }}FrameLowering(const {{ namespace }}Subtarget &STI)
      : TargetFrameLowering(StackGrowsDown, Align(8), 0), STI(STI) {}

  void emitPrologue(MachineFunction &MF, MachineBasicBlock &MBB) const override;
  void emitEpilogue(MachineFunction &MF, MachineBasicBlock &MBB) const override;

  bool hasFP(const MachineFunction &MF) const override;
  void determineCalleeSaves(MachineFunction &MF, BitVector &SavedRegs,
                            RegScavenger *RS) const override;

  MachineBasicBlock::iterator
  eliminateCallFramePseudoInstr(MachineFunction &MF, MachineBasicBlock &MBB,
                                MachineBasicBlock::iterator MI) const override {
    return MBB.erase(MI);
  }

protected:
  const {{ namespace }}Subtarget &STI;
};
}
#endif
