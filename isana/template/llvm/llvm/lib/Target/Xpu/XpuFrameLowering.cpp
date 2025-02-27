//===-- {{ Xpu }}FrameLowering.cpp - {{ Xpu }} Frame Information -*- C++ -*-===//

#include "{{ Xpu }}FrameLowering.h"
#include "{{ Xpu }}InstrInfo.h"
#include "{{ Xpu }}Subtarget.h"
#include "llvm/CodeGen/MachineFrameInfo.h"
#include "llvm/CodeGen/MachineFunction.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/CodeGen/MachineRegisterInfo.h"

using namespace llvm;

bool {{ Xpu }}FrameLowering::hasFP(
  const MachineFunction &MF
) const {
  return false;
}

void {{ Xpu }}FrameLowering::emitPrologue(
  MachineFunction &MF,
  MachineBasicBlock &MBB
) const {
  MachineFrameInfo &MFI = MF.getFrameInfo();
  MachineBasicBlock::iterator MBBI = MBB.begin();
  const auto &TII = *static_cast<const {{ Xpu }}InstrInfo *>(STI.getInstrInfo());

  // Debug location must be unknown since the first debug location is used
  // to determine the end of the prologue.
  DebugLoc DL;

  uint64_t StackSize = MFI.getStackSize();

  if (StackSize == 0 && !MFI.adjustsStack())
    return;

  Register DstReg = {{ Xpu }}::{{ sp }};
  Register SrcReg = {{ Xpu }}::{{ sp }};
  TII.addImmediate(DstReg, SrcReg, -StackSize, MBB, MBBI);
}

void {{ Xpu }}FrameLowering::emitEpilogue(
  MachineFunction &MF,
  MachineBasicBlock &MBB
) const {
  MachineFrameInfo &MFI = MF.getFrameInfo();
  MachineBasicBlock::iterator MBBI = MBB.getLastNonDebugInstr();
  const auto &TII = *static_cast<const {{ Xpu }}InstrInfo *>(STI.getInstrInfo());

  DebugLoc DL;

  uint64_t StackSize = MFI.getStackSize();

  if (StackSize == 0)
    return;

  Register DstReg = {{ Xpu }}::{{ sp }};
  Register SrcReg = {{ Xpu }}::{{ sp }};
  TII.addImmediate(DstReg, SrcReg, StackSize, MBB, MBBI);
}

void {{ Xpu }}FrameLowering::determineCalleeSaves(
  MachineFunction &MF,
  BitVector &SavedRegs,
  RegScavenger *RS
) const {
  TargetFrameLowering::determineCalleeSaves(MF, SavedRegs, RS);
}
