//===-- {{ Xpu }}RegisterInfo.cpp - {{ Xpu }} Register Information -*- C++ -*-===//

#include "{{ Xpu }}RegisterInfo.h"
#include "{{ Xpu }}.h"
#include "{{ Xpu }}Subtarget.h"
#include "llvm/CodeGen/MachineFrameInfo.h"
#include "llvm/CodeGen/MachineFunction.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/CodeGen/RegisterScavenging.h"
#include "llvm/CodeGen/TargetFrameLowering.h"
#include "llvm/CodeGen/TargetInstrInfo.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/ErrorHandling.h"

using namespace llvm;

#define DEBUG_TYPE "{{ xpu }}-reg-info"

#define GET_REGINFO_TARGET_DESC
#include "{{ Xpu }}GenRegisterInfo.inc"

{{ Xpu }}RegisterInfo::{{ Xpu }}RegisterInfo()
    : {{ Xpu }}GenRegisterInfo({{ Xpu }}::{{ reg0 }}) {}

const MCPhysReg *
{{ Xpu }}RegisterInfo::getCalleeSavedRegs(const MachineFunction *MF) const {
  return CSR_ABI0_SaveList;
}

const uint32_t *
{{ Xpu }}RegisterInfo::getCallPreservedMask(const MachineFunction &MF,
                                            CallingConv::ID CC) const {
  return CSR_ABI0_RegMask;
}

BitVector
{{ Xpu }}RegisterInfo::getReservedRegs(const MachineFunction &MF) const {
  BitVector Reserved(getNumRegs());
  {% for reg in reserved_regs -%}
  markSuperRegs(Reserved, {{ Xpu }}::{{ reg }});
  {% endfor -%}
  return Reserved;
}

bool
{{ Xpu }}RegisterInfo::eliminateFrameIndex(MachineBasicBlock::iterator MBBI,
                                           int SPAdj, unsigned FIOperandNum,
                                           RegScavenger *RS) const {
  MachineInstr &MI = *MBBI;
  MachineBasicBlock &MBB = *MI.getParent();
  MachineFunction &MF = *MBB.getParent();

  unsigned i = 0;
  while (!MI.getOperand(i).isFI()) {
    ++i;
    assert(i < MI.getNumOperands() && "Instr doesn't have FrameIndex operand!");
  }

  Register FrameReg = {{ Xpu }}::X2;
  int FrameIndex = MI.getOperand(FIOperandNum).getIndex();
  uint64_t StackSize = MF.getFrameInfo().getStackSize();
  int64_t SpOffset = MF.getFrameInfo().getObjectOffset(FrameIndex);

  // before:
  //   lui  t0, imm_hi
  //   addi t1, t0, imm_lo
  //   add  dst, frame_addr, t1
  // aftter:
  //   lui  t0, imm_hi+off_hi
  //   addi t1, t0, imm_lo+off_lo
  //   add  dst, x2, t1
  MachineInstr *Lui = nullptr;
  MachineInstr *Addi = nullptr;
  Register RegT1 = MI.getOperand(i+1).getReg();
  Register RegT0;
  auto II = MBBI.getReverse();
  for (; II != MBB.rend(); II++) {
    MachineInstr &MII = *II;
    if (MII.getOpcode() == {{ Xpu }}::ADDI && MII.getOperand(0).getReg() == RegT1) {
      Addi = &MII;
      RegT0 = MII.getOperand(1).getReg();
      break;
    }
  }
  for (; II != MBB.rend(); II++) {
    MachineInstr &MII = *II;
    if (MII.getOpcode() == {{ Xpu }}::LUI && MII.getOperand(0).getReg() == RegT0) {
      Lui = &MII;
      break;
    }
  }
  assert ((Lui && Addi) && "FrameIndex should be converted to LUI & ADDI & ADD");

  int64_t OldHi20 = Lui->getOperand(1).getImm();
  int64_t OldLo12 = Addi->getOperand(2).getImm();
  int64_t OldValue = (OldHi20 << 12) + OldLo12;

  int64_t NewValue = SpOffset + (int64_t)StackSize;
  NewValue += OldValue;

  int64_t NewLo12 = SignExtend64<12>(NewValue);
  int64_t NewHi20 = ((NewValue - NewLo12) >> 12);

  Lui->getOperand(1).setImm(NewHi20);
  Addi->getOperand(2).setImm(NewLo12);
  MI.getOperand(i+0).ChangeToRegister(FrameReg, false);

  return false;
}

Register
{{ Xpu }}RegisterInfo::getFrameRegister(const MachineFunction &MF) const {
  const TargetFrameLowering *TFI = getFrameLowering(MF);
  return TFI->hasFP(MF) ? {{ Xpu }}::{{ fp }} : {{ Xpu }}::{{ sp }};
}
