//===-- {{ namespace }}TargetMachine.cpp - Define TargetMachine for {{ namespace }} --===//
#include "{{ namespace }}TargetMachine.h"
#include "TargetInfo/{{ namespace }}TargetInfo.h"
#include "llvm/ADT/STLExtras.h"
#include "llvm/CodeGen/Passes.h"
#include "llvm/CodeGen/TargetLoweringObjectFileImpl.h"
#include "llvm/CodeGen/TargetPassConfig.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Support/FormattedStream.h"
#include "llvm/Target/TargetOptions.h"
#include <optional>
using namespace llvm;

extern "C" void LLVMInitialize{{ namespace }}Target() {
  RegisterTargetMachine<{{ namespace }}TargetMachine> Z(getThe{{ namespace }}32leTarget());
  RegisterTargetMachine<{{ namespace }}TargetMachine> Y(getThe{{ namespace }}32beTarget());
  RegisterTargetMachine<{{ namespace }}TargetMachine> X(getThe{{ namespace }}64leTarget());
  RegisterTargetMachine<{{ namespace }}TargetMachine> W(getThe{{ namespace }}64beTarget());

  PassRegistry *Registry = PassRegistry::getPassRegistry();
  initialize{{ namespace }}DAGToDAGISelLegacyPass(*Registry);
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

{{ namespace }}TargetMachine::{{ namespace }}TargetMachine(
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
class {{ namespace }}PassConfig : public TargetPassConfig {
public:
  {{ namespace }}PassConfig({{ namespace }}TargetMachine &TM, PassManagerBase &PM)
      : TargetPassConfig(TM, PM) {}

  {{ namespace }}TargetMachine &get{{ namespace }}TargetMachine() const {
    return getTM<{{ namespace }}TargetMachine>();
  }

  bool addInstSelector() override;
};
}

bool {{ namespace }}PassConfig::addInstSelector() {
  addPass(create{{ namespace }}ISelDag(get{{ namespace }}TargetMachine(), getOptLevel()));

  return false;
}

TargetPassConfig *{{ namespace }}TargetMachine::createPassConfig(PassManagerBase &PM) {
  return new {{ namespace }}PassConfig(*this, PM);
}
