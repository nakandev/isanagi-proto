//===-- {{ namespace }}TargetMachine.h - Define TargetMachine for {{ namespace }} --===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}TARGETMACHINE_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}TARGETMACHINE_H

#include "{{ namespace }}Subtarget.h"
#include "llvm/CodeGen/SelectionDAGTargetInfo.h"
#include "llvm/IR/DataLayout.h"
#include "llvm/Target/TargetMachine.h"
#include <optional>

namespace llvm {
class {{ namespace }}TargetMachine : public LLVMTargetMachine {
  std::unique_ptr<TargetLoweringObjectFile> TLOF;
  {{ namespace }}Subtarget Subtarget;

public:
  {{ namespace }}TargetMachine(const Target &T, const Triple &TT, StringRef CPU,
                         StringRef FS, const TargetOptions &Options,
                         std::optional<Reloc::Model> RM,
                         std::optional<CodeModel::Model> CM, CodeGenOptLevel OL,
                         bool JIT);

  const {{ namespace }}Subtarget *getSubtargetImpl() const { return &Subtarget; }
  const {{ namespace }}Subtarget *getSubtargetImpl(const Function &) const override {
    return &Subtarget;
  }

  TargetPassConfig *createPassConfig(PassManagerBase &PM) override;

  TargetLoweringObjectFile *getObjFileLowering() const override {
    return TLOF.get();
  }
};
} // namespace llvm

#endif
