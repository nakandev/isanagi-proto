//===-- {{ Xpu }}TargetMachine.cpp - Define TargetMachine for {{ Xpu }} --===//

#include "{{ Xpu }}TargetMachine.h"
#include "TargetInfo/{{ Xpu }}TargetInfo.h"
#include "llvm/ADT/STLExtras.h"
#include "llvm/CodeGen/Passes.h"
#include "llvm/CodeGen/TargetLoweringObjectFileImpl.h"
#include "llvm/CodeGen/TargetPassConfig.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Support/FormattedStream.h"
#include "llvm/Target/TargetOptions.h"
#include <optional>
using namespace llvm;

extern "C" void LLVMInitialize{{ Xpu }}Target() {
  RegisterTargetMachine<{{ Xpu }}TargetMachine> Z(getThe{{ Xpu }}32leTarget());
  RegisterTargetMachine<{{ Xpu }}TargetMachine> Y(getThe{{ Xpu }}32beTarget());
  RegisterTargetMachine<{{ Xpu }}TargetMachine> X(getThe{{ Xpu }}64leTarget());
  RegisterTargetMachine<{{ Xpu }}TargetMachine> W(getThe{{ Xpu }}64beTarget());

  PassRegistry *Registry = PassRegistry::getPassRegistry();
  initialize{{ Xpu }}DAGToDAGISelLegacyPass(*Registry);
}

static std::string computeDataLayout(const Triple &TT) {
  return "e"        // Little endian
         "-m:e"     // ELF name manging
         "-p:32:32" // 32-bit pointers, 32 bit aligned
         "-i32:32"  // 32 bit integers, 32 bit aligned
         "-n32"     // 32 bit native integer width
         "-S128";   // 128 bit natural stack alignment
}

static Reloc::Model getEffectiveRelocModel(const Triple &TT,
                                           std::optional<Reloc::Model> RM) {
  return RM.value_or(Reloc::Static);
}

{{ Xpu }}TargetMachine::{{ Xpu }}TargetMachine(
  const Target &T, const Triple &TT,
  StringRef CPU, StringRef FS,
  const TargetOptions &Options,
  std::optional<Reloc::Model> RM,
  std::optional<CodeModel::Model> CM,
  CodeGenOptLevel OL, bool JIT)
: LLVMTargetMachine(
    T, computeDataLayout(TT), TT, CPU, FS, Options,
    getEffectiveRelocModel(TT, RM),
    getEffectiveCodeModel(CM, CodeModel::Small), OL
  ),
  TLOF(std::make_unique<TargetLoweringObjectFileELF>()),
  Subtarget(TT, CPU, FS, *this)
{
  initAsmInfo();
}

namespace {
class {{ Xpu }}PassConfig : public TargetPassConfig {
public:
  {{ Xpu }}PassConfig({{ Xpu }}TargetMachine &TM, PassManagerBase &PM)
      : TargetPassConfig(TM, PM) {}

  {{ Xpu }}TargetMachine &get{{ Xpu }}TargetMachine() const {
    return getTM<{{ Xpu }}TargetMachine>();
  }

  bool addInstSelector() override;
};
}

bool {{ Xpu }}PassConfig::addInstSelector() {
  addPass(create{{ Xpu }}ISelDag(get{{ Xpu }}TargetMachine(), getOptLevel()));

  return false;
}

TargetPassConfig *{{ Xpu }}TargetMachine::createPassConfig(PassManagerBase &PM) {
  return new {{ Xpu }}PassConfig(*this, PM);
}
