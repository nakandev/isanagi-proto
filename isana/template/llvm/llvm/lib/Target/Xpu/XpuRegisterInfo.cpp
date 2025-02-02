//===-- {{ namespace }}RegisterInfo.cpp - {{ namespace }} Register Information -*- C++ -*-===//

#include "{{ namespace }}RegisterInfo.h"
#include "{{ namespace }}.h"
#include "{{ namespace }}Subtarget.h"
#include "llvm/CodeGen/MachineFrameInfo.h"
#include "llvm/CodeGen/MachineFunction.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/CodeGen/RegisterScavenging.h"
#include "llvm/CodeGen/TargetFrameLowering.h"
#include "llvm/CodeGen/TargetInstrInfo.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/ErrorHandling.h"

using namespace llvm;

#define DEBUG_TYPE "{{ namespace.lower() }}-reg-info"

#define GET_REGINFO_TARGET_DESC
#include "{{ namespace }}GenRegisterInfo.inc"

{{ namespace }}RegisterInfo::{{ namespace }}RegisterInfo()
    : {{ namespace }}GenRegisterInfo({{ namespace }}::{{ reg0 }}) {}

const MCPhysReg *
{{ namespace }}RegisterInfo::getCalleeSavedRegs(const MachineFunction *MF) const {
  return CSR_ABI0_SaveList;
}

const uint32_t *
{{ namespace }}RegisterInfo::getCallPreservedMask(const MachineFunction &MF,
                                            CallingConv::ID CC) const {
  return CSR_ABI0_RegMask;
}

BitVector
{{ namespace }}RegisterInfo::getReservedRegs(const MachineFunction &MF) const {
  BitVector Reserved(getNumRegs());
  {% for reg in reserved_regs -%}
  markSuperRegs(Reserved, CustomXPU::{{ reg }});
  {% endfor -%}
  return Reserved;
}

bool
{{ namespace }}RegisterInfo::eliminateFrameIndex(MachineBasicBlock::iterator II,
                                           int SPAdj, unsigned FIOperandNum,
                                           RegScavenger *RS) const {
  // MachineInstr *MI = &*II;
  // MachineBasicBlock &MBB = *MI->getParent();
  // MachineFunction &MF = *MI->getParent()->getParent();
  // MachineRegisterInfo &MRI = MF.getRegInfo();
  // const {{ namespace }}InstrInfo *TII = MF.getSubtarget<{{ namespace }}Subtarget>().getInstrInfo();
  // DebugLoc DL = MI->getDebugLoc();
  // const {{ namespace }}Subtarget &STI = MF.getSubtarget<{{ namespace }}Subtarget>();
  // 
  // Register NewReg1 = MRI.createVirtualRegister(&{{ namespace }}::GPRRegClass);
  // Register NewReg2 = MRI.createVirtualRegister(&{{ namespace }}::GPRRegClass);
  // BuildMI(MBB, II, DL, TII->get({{ namespace }}::ADD),
  //         MI->getOperand(0).getReg())
  //     .addReg(NewReg1, RegState::Define)
  //     .addReg(NewReg2, RegState::Define);

  return false;
}

Register
{{ namespace }}RegisterInfo::getFrameRegister(const MachineFunction &MF) const {
  return {{ namespace }}::{{ fp }};
}
