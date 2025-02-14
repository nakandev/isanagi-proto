//===-- {{ namespace }}InstrInfo.cpp - {{ namespace }} Instruction Information -*- C++ -*-===//

#include "{{ namespace }}InstrInfo.h"
#include "{{ namespace }}.h"
#include "{{ namespace }}Subtarget.h"
#include "llvm/ADT/SmallVector.h"
#include "llvm/CodeGen/MachineBasicBlock.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/IR/DebugLoc.h"
#include "llvm/Support/ErrorHandling.h"
#include <cassert>
#include <iterator>

#define GET_INSTRINFO_CTOR_DTOR
#include "{{ namespace }}GenInstrInfo.inc"

using namespace llvm;

{{ namespace }}InstrInfo::{{ namespace }}InstrInfo({{ namespace }}Subtarget &STI)
    : {{ namespace }}GenInstrInfo(/*{{ namespace }}::ADJCALLSTACKDOWN, {{ namespace }}::ADJCALLSTACKUP*/),
      STI(STI) {}

bool
{{ namespace }}InstrInfo::expandPostRAPseudo(MachineInstr &MI) const {
  auto &MBB = *MI.getParent();

  switch(MI.getDesc().getOpcode()) {
    default:
      return false;
    case {{ namespace }}::PseudoRET:
      expandPseudoRET(MBB, MI);
      break;
  }

  MBB.erase(MI);
  return true;
}

void
{{ namespace }}InstrInfo::expandPseudoRET(
  MachineBasicBlock &MBB,
  MachineBasicBlock::iterator I
) const {
  BuildMI(MBB, I, I->getDebugLoc(), get({{ namespace }}::JALR))
    .addReg({{ namespace }}::X0).addReg({{ namespace }}::X1).addImm(0);
}

void
{{ namespace }}InstrInfo::addImmediate(
  Register DstReg,
  Register SrcReg,
  int64_t Amount,
  MachineBasicBlock &MBB,
  MachineBasicBlock::iterator MBBI
) const {
  DebugLoc DL = MBBI != MBB.end() ? MBBI->getDebugLoc() : DebugLoc();

  if (isInt<12>(Amount)) {
    BuildMI(MBB, MBBI, DL, get({{ namespace }}::ADDI), DstReg)
      .addReg(SrcReg)
      .addImm(Amount);
  } else {
    MachineFunction *MF = MBB.getParent();
    MachineRegisterInfo &MRI = MF->getRegInfo();

    Register TempReg = MRI.createVirtualRegister(&{{ namespace }}::GPRRegClass);
    Register ImmReg = MRI.createVirtualRegister(&{{ namespace }}::GPRRegClass);
    int64_t Lo12 = SignExtend64<12>(Amount);
    int64_t Hi20 = ((Amount - Lo12) >> 12);

    BuildMI(MBB, MBBI, DL, get({{ namespace }}::LUI), TempReg)
      .addImm(Hi20);
    BuildMI(MBB, MBBI, DL, get({{ namespace }}::ADDI), ImmReg)
      .addReg(TempReg, RegState::Kill)
      .addImm(Lo12);
    BuildMI(MBB, MBBI, DL, get({{ namespace }}::ADD), DstReg)
      .addReg(SrcReg)
      .addReg(ImmReg, RegState::Kill);
  }
}

void
{{ namespace }}InstrInfo::copyPhysReg(
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

  if ({{ namespace }}::GPRRegClass.contains(DstReg, SrcReg)) {
    BuildMI(MBB, MBBI, DL, get({{ namespace }}::ADDI), DstReg)
        .addReg(SrcReg,
                getKillRegState(KillSrc) | getRenamableRegState(RenamableSrc))
        .addImm(0);
    return;
  }
}
