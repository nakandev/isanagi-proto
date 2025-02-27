//===-- {{ Xpu }}InstrInfo.cpp - {{ Xpu }} Instruction Information -*- C++ -*-===//

#include "{{ Xpu }}InstrInfo.h"
#include "{{ Xpu }}.h"
// #include "{{ Xpu }}MachineFunctionInfo.h"
#include "llvm/CodeGen/MachineFrameInfo.h"
#include "{{ Xpu }}Subtarget.h"
#include "llvm/ADT/SmallVector.h"
#include "llvm/CodeGen/MachineBasicBlock.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/IR/DebugLoc.h"
#include "llvm/Support/ErrorHandling.h"
#include <cassert>
#include <iterator>

#define GET_INSTRINFO_CTOR_DTOR
#include "{{ Xpu }}GenInstrInfo.inc"

using namespace llvm;

{{ Xpu }}InstrInfo::{{ Xpu }}InstrInfo({{ Xpu }}Subtarget &STI)
    : {{ Xpu }}GenInstrInfo({{ Xpu }}::ADJCALLSTACKDOWN, {{ Xpu }}::ADJCALLSTACKUP),
      STI(STI) {}

bool
{{ Xpu }}InstrInfo::expandPostRAPseudo(MachineInstr &MI) const {
  auto &MBB = *MI.getParent();

  switch(MI.getDesc().getOpcode()) {
    default:
      return false;
    case {{ Xpu }}::PseudoRET:
      expandPseudoRET(MBB, MI);
      break;
  }

  MBB.erase(MI);
  return true;
}

void
{{ Xpu }}InstrInfo::expandPseudoRET(
  MachineBasicBlock &MBB,
  MachineBasicBlock::iterator I
) const {
  BuildMI(MBB, I, I->getDebugLoc(), get({{ Xpu }}::JALR))
    .addReg({{ Xpu }}::X0).addReg({{ Xpu }}::X1).addImm(0);
}

void
{{ Xpu }}InstrInfo::addImmediate(
  Register DstReg,
  Register SrcReg,
  int64_t Amount,
  MachineBasicBlock &MBB,
  MachineBasicBlock::iterator MBBI
) const {
  DebugLoc DL = MBBI != MBB.end() ? MBBI->getDebugLoc() : DebugLoc();

  if (isInt<12>(Amount)) {
    BuildMI(MBB, MBBI, DL, get({{ Xpu }}::ADDI), DstReg)
      .addReg(SrcReg)
      .addImm(Amount);
  } else {
    MachineFunction *MF = MBB.getParent();
    MachineRegisterInfo &MRI = MF->getRegInfo();

    Register TempReg = MRI.createVirtualRegister(&{{ Xpu }}::GPRRegClass);
    Register ImmReg = MRI.createVirtualRegister(&{{ Xpu }}::GPRRegClass);
    int64_t Lo12 = SignExtend64<12>(Amount);
    int64_t Hi20 = ((Amount - Lo12) >> 12);

    BuildMI(MBB, MBBI, DL, get({{ Xpu }}::LUI), TempReg)
      .addImm(Hi20);
    BuildMI(MBB, MBBI, DL, get({{ Xpu }}::ADDI), ImmReg)
      .addReg(TempReg, RegState::Kill)
      .addImm(Lo12);
    BuildMI(MBB, MBBI, DL, get({{ Xpu }}::ADD), DstReg)
      .addReg(SrcReg)
      .addReg(ImmReg, RegState::Kill);
  }
}

void
{{ Xpu }}InstrInfo::copyPhysReg(
  MachineBasicBlock &MBB,
  MachineBasicBlock::iterator MBBI,
  const DebugLoc &DL,
  MCRegister DstReg,
  MCRegister SrcReg,
  bool KillSrc,
  bool RenamableDest,
  bool RenamableSrc
) const {
  const TargetRegisterInfo *TRI = STI.getRegisterInfo();

  if ({{ Xpu }}::GPRRegClass.contains(DstReg, SrcReg)) {
    BuildMI(MBB, MBBI, DL, get({{ Xpu }}::ADDI), DstReg)
        .addReg(SrcReg,
                getKillRegState(KillSrc) | getRenamableRegState(RenamableSrc))
        .addImm(0);
    return;
  }
}

void
{{ Xpu }}InstrInfo::storeRegToStackSlot(
  MachineBasicBlock &MBB,
  MachineBasicBlock::iterator I,
  Register SrcReg, bool IsKill, int FI,
  const TargetRegisterClass *RC,
  const TargetRegisterInfo *TRI,
  Register VReg
) const {
  MachineFunction *MF = MBB.getParent();
  MachineFrameInfo &MFI = MF->getFrameInfo();

  unsigned Opcode = {{ Xpu }}::SW;
  MachineMemOperand *MMO = MF->getMachineMemOperand(
      MachinePointerInfo::getFixedStack(*MF, FI), MachineMemOperand::MOStore,
      MFI.getObjectSize(FI), MFI.getObjectAlign(FI));

  BuildMI(MBB, I, DebugLoc(), get(Opcode))
      .addReg(SrcReg, getKillRegState(IsKill))
      .addFrameIndex(FI)
      .addImm(0)
      .addMemOperand(MMO);
}

void
{{ Xpu }}InstrInfo::loadRegFromStackSlot(
  MachineBasicBlock &MBB,
  MachineBasicBlock::iterator I,
  Register DstReg, int FI,
  const TargetRegisterClass *RC,
  const TargetRegisterInfo *TRI,
  Register VReg
) const {
  MachineFunction *MF = MBB.getParent();
  MachineFrameInfo &MFI = MF->getFrameInfo();

  unsigned Opcode = {{ Xpu }}::LW;
  MachineMemOperand *MMO = MF->getMachineMemOperand(
      MachinePointerInfo::getFixedStack(*MF, FI), MachineMemOperand::MOLoad,
      MFI.getObjectSize(FI), MFI.getObjectAlign(FI));

  BuildMI(MBB, I, DebugLoc(), get(Opcode), DstReg)
      .addFrameIndex(FI)
      .addImm(0)
      .addMemOperand(MMO);
}
