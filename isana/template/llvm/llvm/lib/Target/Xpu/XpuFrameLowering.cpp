//===-- {{ namespace }}FrameLowering.cpp - {{ namespace }} Frame Information -*- C++ -*-===//

#include "{{ namespace }}FrameLowering.h"
#include "{{ namespace }}InstrInfo.h"
#include "{{ namespace }}Subtarget.h"
#include "llvm/CodeGen/MachineFrameInfo.h"
#include "llvm/CodeGen/MachineFunction.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/CodeGen/MachineRegisterInfo.h"

using namespace llvm;

bool {{ namespace }}FrameLowering::hasFP(
  const MachineFunction &MF
) const {
  return false;
}

void {{ namespace }}FrameLowering::emitPrologue(
  MachineFunction &MF,
  MachineBasicBlock &MBB
) const {
  MachineFrameInfo &MFI = MF.getFrameInfo();
  MachineBasicBlock::iterator MBBI = MBB.begin();
  const auto &TII = *static_cast<const {{ namespace }}InstrInfo *>(STI.getInstrInfo());

  // Debug location must be unknown since the first debug location is used
  // to determine the end of the prologue.
  DebugLoc DL;

  uint64_t StackSize = MFI.getStackSize();

  if (StackSize == 0 && !MFI.adjustsStack())
    return;

  Register DstReg = {{ namespace }}::{{ sp }};
  Register SrcReg = {{ namespace }}::{{ sp }};
  TII.addImmediate(DstReg, SrcReg, -StackSize, MBB, MBBI);
}

void {{ namespace }}FrameLowering::emitEpilogue(
  MachineFunction &MF,
  MachineBasicBlock &MBB
) const {
  MachineFrameInfo &MFI = MF.getFrameInfo();
  MachineBasicBlock::iterator MBBI = MBB.getLastNonDebugInstr();
  const auto &TII = *static_cast<const {{ namespace }}InstrInfo *>(STI.getInstrInfo());

  DebugLoc DL;

  uint64_t StackSize = MFI.getStackSize();

  if (StackSize == 0)
    return;

  Register DstReg = {{ namespace }}::{{ sp }};
  Register SrcReg = {{ namespace }}::{{ sp }};
  TII.addImmediate(DstReg, SrcReg, StackSize, MBB, MBBI);
}

void {{ namespace }}FrameLowering::determineCalleeSaves(
  MachineFunction &MF,
  BitVector &SavedRegs,
  RegScavenger *RS
) const {
  TargetFrameLowering::determineCalleeSaves(MF, SavedRegs, RS);
}
