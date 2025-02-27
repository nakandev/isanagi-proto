//===-- {{ Xpu }}.h - Top-level interface for {{ Xpu }} representation --*- C++ -*-===//

#ifndef LLVM_LIB_TARGET_{{ XPU }}_{{ XPU }}_H
#define LLVM_LIB_TARGET_{{ XPU }}_{{ XPU }}_H

#include "MCTargetDesc/{{ Xpu }}MCTargetDesc.h"
#include "llvm/Target/TargetMachine.h"

namespace llvm {
class {{ Xpu }}TargetMachine;
class FunctionPass;
class PassRegistry;

FunctionPass *create{{ Xpu }}ISelDag({{ Xpu }}TargetMachine &TM,
                                CodeGenOptLevel OptLevel);
void initialize{{ Xpu }}DAGToDAGISelLegacyPass(PassRegistry &);
} // namespace llvm

#endif
