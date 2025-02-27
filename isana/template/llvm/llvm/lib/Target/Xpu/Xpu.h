//===-- {{ namespace }}.h - Top-level interface for {{ namespace }} representation --*- C++ -*-===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}_H

#include "MCTargetDesc/{{ namespace }}MCTargetDesc.h"
#include "llvm/Target/TargetMachine.h"

namespace llvm {
class {{ namespace }}TargetMachine;
class FunctionPass;
class PassRegistry;

FunctionPass *create{{ namespace }}ISelDag({{ namespace }}TargetMachine &TM,
                                CodeGenOptLevel OptLevel);
void initialize{{ namespace }}DAGToDAGISelLegacyPass(PassRegistry &);
} // namespace llvm

#endif
