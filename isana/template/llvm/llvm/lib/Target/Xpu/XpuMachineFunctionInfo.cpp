//=- {{ Xpu }}MachineFunctionInfo.cpp - {{ Xpu }} machine function info --*- C++ -*-=//

#include "{{ Xpu }}MachineFunctionInfo.h"

#include "{{ Xpu }}InstrInfo.h"
#include "{{ Xpu }}Subtarget.h"
#include "llvm/IR/Function.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/CodeGen/MachineRegisterInfo.h"
#include "llvm/CodeGen/PseudoSourceValue.h"
#include "llvm/CodeGen/PseudoSourceValueManager.h"

using namespace llvm;

bool FixGlobalBaseReg;

MachineFunctionInfo *
{{ Xpu }}MachineFunctionInfo::clone(BumpPtrAllocator &Allocator, MachineFunction &DestMF,
                        const DenseMap<MachineBasicBlock *, MachineBasicBlock *>
                            &Src2DstMBB) const {
  return DestMF.cloneInfo<{{ Xpu }}MachineFunctionInfo>(*this);
}

{{ Xpu }}MachineFunctionInfo::~{{ Xpu }}MachineFunctionInfo() = default;
