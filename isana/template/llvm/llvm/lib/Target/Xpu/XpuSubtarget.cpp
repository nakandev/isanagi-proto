//===-- {{ namespace }}Subtarget.cpp - {{ namespace }} Subtarget Information Impl -*- C++ -*-===//

#include "{{ namespace }}Subtarget.h"
#include "{{ namespace }}.h"
#include "{{ namespace }}TargetMachine.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/TargetParser/Host.h"

using namespace llvm;

#define DEBUG_TYPE "{{ namespace.lower() }}-subtarget"

#define GET_SUBTARGETINFO_TARGET_DESC
#define GET_SUBTARGETINFO_CTOR
#include "{{ namespace }}GenSubtargetInfo.inc"

void {{ namespace }}Subtarget::anchor() {}

{{ namespace }}Subtarget &
{{ namespace }}Subtarget::initializeSubtargetDependencies(
  StringRef CPU,
  StringRef FS
) {
  Has64Bit = false;
  HasBigEndian = false;
  ParseSubtargetFeatures(CPU, /*TuneCPU*/ CPU, FS);
  return *this;
}

{{ namespace }}Subtarget::{{ namespace }}Subtarget(
  const Triple &TT, StringRef CPU, StringRef FS, const TargetMachine &TM)
    : {{ namespace }}GenSubtargetInfo(TT, CPU, /*TuneCPU*/ CPU, FS),
      FrameLowering(initializeSubtargetDependencies(CPU, FS)),
      InstrInfo(*this), RegInfo(), TLInfo(TM, *this) {
}
