//=- {{ XPU }}MachineFunctionInfo.h - {{ Xpu }} machine function info -*- C++ -*-=//
//
//===----------------------------------------------------------------------===//
//
// This file declares {{ XPU }}-specific per-machine-function information.
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_LIB_TARGET_{{ XPU }}_{{ XPU }}MACHINEFUNCTIONINFO_H
#define LLVM_LIB_TARGET_{{ XPU }}_{{ XPU }}MACHINEFUNCTIONINFO_H

#include "llvm/CodeGen/MachineFrameInfo.h"
#include "llvm/CodeGen/MachineFunction.h"
#include "llvm/CodeGen/MachineMemOperand.h"
#include "llvm/CodeGen/TargetFrameLowering.h"
#include "llvm/Target/TargetMachine.h"
#include <map>

namespace llvm {

class {{ Xpu }}MachineFunctionInfo : public MachineFunctionInfo {
public:
  {{ Xpu }}MachineFunctionInfo(const Function &F, const TargetSubtargetInfo *STI) {}

  MachineFunctionInfo *
  clone(BumpPtrAllocator &Allocator, MachineFunction &DestMF,
        const DenseMap<MachineBasicBlock *, MachineBasicBlock *> &Src2DstMBB)
      const override;

  ~{{ Xpu }}MachineFunctionInfo();

  int getVarArgsFrameIndex() const { return VarArgsFrameIndex; }
  void setVarArgsFrameIndex(int Index) { VarArgsFrameIndex = Index; }

  unsigned getVarArgsSaveSize() const { return VarArgsSaveSize; }
  void setVarArgsSaveSize(int Size) { VarArgsSaveSize = Size; }

  /// True if function has a byval argument.
  bool HasByvalArg;

  /// Size of incoming argument area.
  unsigned IncomingArgSize;

  void setFormalArgInfo(unsigned Size, bool HasByval) {
    IncomingArgSize = Size;
    HasByvalArg = HasByval;
  }

  unsigned getIncomingArgSize() const { return IncomingArgSize; }
  bool hasByvalArg() const { return HasByvalArg; }

private:
  /// VarArgsFrameIndex - FrameIndex for start of varargs area.
  int VarArgsFrameIndex;
  int VarArgsSaveSize;
};

} // end of namespace llvm

#endif // {{ XPU }}_MACHINE_FUNCTION_INFO_H
