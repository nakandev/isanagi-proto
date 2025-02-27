//===- {{ namespace }}MCTargetDesc.cpp - {{ namespace }} Target Descriptions -===//

#include "{{ namespace }}MCTargetDesc.h"
#include "{{ namespace }}AsmBackend.h"
// #include "{{ namespace }}BaseInfo.h"
// #include "{{ namespace }}ELFStreamer.h"
#include "{{ namespace }}InstPrinter.h"
#include "{{ namespace }}MCAsmInfo.h"
#include "TargetInfo/{{ namespace }}TargetInfo.h"

#include "llvm/MC/MachineLocation.h"
#include "llvm/MC/MCAsmBackend.h"
#include "llvm/MC/MCAsmInfo.h"
#include "llvm/MC/MCCodeEmitter.h"
#include "llvm/MC/MCELFStreamer.h"
#include "llvm/MC/MCInstrAnalysis.h"
#include "llvm/MC/MCInstPrinter.h"
#include "llvm/MC/MCInstrInfo.h"
#include "llvm/MC/MCObjectFileInfo.h"
#include "llvm/MC/MCObjectWriter.h"
#include "llvm/MC/MCRegisterInfo.h"
#include "llvm/MC/MCSubtargetInfo.h"
#include "llvm/MC/MCSymbol.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/Support/ErrorHandling.h"

using namespace llvm;

#define GET_INSTRINFO_MC_DESC
#define ENABLE_INSTR_PREDICATE_VERIFIER
#include "{{ namespace }}GenInstrInfo.inc"

#define GET_SUBTARGETINFO_MC_DESC
#include "{{ namespace }}GenSubtargetInfo.inc"

#define GET_REGINFO_MC_DESC
#include "{{ namespace }}GenRegisterInfo.inc"

static MCInstrInfo *create{{ namespace }}MCInstrInfo() {
  MCInstrInfo *X = new MCInstrInfo();
  Init{{ namespace }}MCInstrInfo(X); // defined in {{ namespace }}GenInstrInfo.inc
  return X;
}

static MCRegisterInfo *create{{ namespace }}MCRegisterInfo(const Triple &TT) {
  MCRegisterInfo *X = new MCRegisterInfo();
  Init{{ namespace }}MCRegisterInfo(X, {{ namespace }}::X1); // defined in {{ namespace }}GenRegisterInfo.inc
  return X;
}

static MCSubtargetInfo *create{{ namespace }}MCSubtargetInfo(const Triple &TT,
                                                      StringRef CPU, StringRef FS) {
  if (CPU.empty() || CPU == "generic") {
    if (TT.getArch() == llvm::Triple::{{ namespace.lower() }}64be)
      CPU = "xpu-64be";
    else if (TT.getArch() == llvm::Triple::{{ namespace.lower() }}64le)
      CPU = "xpu-64le";
    else if (TT.getArch() == llvm::Triple::{{ namespace.lower() }}32be)
      CPU = "xpu-32be";
    else if (TT.getArch() == llvm::Triple::{{ namespace.lower() }}32le)
      CPU = "xpu-32le";
  }
  return create{{ namespace }}MCSubtargetInfoImpl(TT, CPU, /*TuneCPU*/CPU ,FS);
}

static MCAsmInfo *create{{ namespace }}MCAsmInfo(const MCRegisterInfo &MRI,
                                           const Triple &TT,
                                           const MCTargetOptions &Options) {
  MCAsmInfo *MAI = new {{ namespace }}MCAsmInfo(TT);
  unsigned SP = MRI.getDwarfRegNum({{ namespace }}::X2, true);
  MCCFIInstruction Inst = MCCFIInstruction::cfiDefCfa(nullptr, SP, 0);
  MAI->addInitialFrameState(Inst);
  return MAI;
}

static MCInstPrinter *create{{ namespace }}MCInstPrinter(const Triple &T,
                                                   unsigned SyntaxVariant,
                                                   const MCAsmInfo &MAI,
                                                   const MCInstrInfo &MII,
                                                   const MCRegisterInfo &MRI) {
 return new {{ namespace }}InstPrinter(MAI, MII, MRI);
}

namespace {

class {{ namespace }}MCInstrAnalysis : public MCInstrAnalysis {
 public:
  {{ namespace }}MCInstrAnalysis(const MCInstrInfo *Info) : MCInstrAnalysis(Info) {}
};
}

static MCInstrAnalysis *create{{ namespace }}MCInstrAnalysis(const MCInstrInfo *Info) {
  return new {{ namespace }}MCInstrAnalysis(Info);
}

extern "C" LLVM_EXTERNAL_VISIBILITY void LLVMInitialize{{ namespace }}TargetMC() {
  for (Target *T : {&getThe{{ namespace }}32leTarget(), &getThe{{ namespace }}32beTarget(),
                    &getThe{{ namespace }}64leTarget(), &getThe{{ namespace }}64beTarget()}) {
    TargetRegistry::RegisterMCRegInfo(*T, create{{ namespace }}MCRegisterInfo);
    TargetRegistry::RegisterMCInstrInfo(*T, create{{ namespace }}MCInstrInfo);
    TargetRegistry::RegisterMCSubtargetInfo(*T, create{{ namespace }}MCSubtargetInfo);
    TargetRegistry::RegisterMCAsmInfo(*T, create{{ namespace }}MCAsmInfo);
    // TargetRegistry::RegisterMCInstrAnalysis(*T, create{{ namespace }}MCInstrAnalysis);
    TargetRegistry::RegisterMCInstPrinter(*T, create{{ namespace }}MCInstPrinter);
    TargetRegistry::RegisterMCCodeEmitter(*T, create{{ namespace }}MCCodeEmitter);
    TargetRegistry::RegisterMCAsmBackend(*T, create{{ namespace }}AsmBackend);
    // TargetRegistry::RegisterELFStreamer(*T, create{{ namespace }}ELFStreamer);
    // TargetRegistry::RegisterObjectTargetStreamer(*T, create{{ namespace }}ObjectTargetStreamer);
    // TargetRegistry::RegisterAsmTargetStreamer(*T, create{{ namespace }}AsmTargetStreamer);
    // TargetRegistry::RegisterNullTargetStreamer(*T, create{{ namespace }}NullTargetStreamer);
  }
}

