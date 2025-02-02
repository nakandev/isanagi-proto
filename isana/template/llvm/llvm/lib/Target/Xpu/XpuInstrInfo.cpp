//===-- CustomXPUInstrInfo.cpp - CustomXPU Instruction Information ----------*- C++ -*-===//

#include "CustomXPUInstrInfo.h"
#include "CustomXPU.h"
#include "llvm/ADT/SmallVector.h"
#include "llvm/CodeGen/MachineBasicBlock.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/IR/DebugLoc.h"
#include "llvm/Support/ErrorHandling.h"
#include <cassert>
#include <iterator>

#define GET_INSTRINFO_CTOR_DTOR
#include "CustomXPUGenInstrInfo.inc"

using namespace llvm;

CustomXPUInstrInfo::CustomXPUInstrInfo()
    : CustomXPUGenInstrInfo(/*CustomXPU::ADJCALLSTACKDOWN, CustomXPU::ADJCALLSTACKUP*/) {}

bool CustomXPUInstrInfo::expandPostRAPseudo(MachineInstr &MI) const {
  auto &MBB = *MI.getParent();

  switch(MI.getDesc().getOpcode()) {
    default:
      return false;
    case CustomXPU::PseudoRET:
      expandPseudoRET(MBB, MI);
      break;
  }

  MBB.erase(MI);
  return true;
}

void CustomXPUInstrInfo::expandPseudoRET(
  MachineBasicBlock &MBB,
  MachineBasicBlock::iterator I
) const {
  BuildMI(MBB, I, I->getDebugLoc(), get(CustomXPU::JALR))
    .addReg(CustomXPU::X0).addReg(CustomXPU::X1).addImm(0);
}
