//===-- {{ Xpu }}Subtarget.cpp - {{ Xpu }} Subtarget Information Impl -*- C++ -*-===//

#include "{{ Xpu }}Subtarget.h"
#include "{{ Xpu }}.h"
#include "{{ Xpu }}TargetMachine.h"
#include "llvm/MC/TargetRegistry.h"
#include "llvm/TargetParser/Host.h"

using namespace llvm;

#define DEBUG_TYPE "{{ xpu }}-subtarget"

#define GET_SUBTARGETINFO_TARGET_DESC
#define GET_SUBTARGETINFO_CTOR
#include "{{ Xpu }}GenSubtargetInfo.inc"

void {{ Xpu }}Subtarget::anchor() {}

{{ Xpu }}Subtarget &
{{ Xpu }}Subtarget::initializeSubtargetDependencies(
  StringRef CPU,
  StringRef FS
) {
  Has64Bit = false;
  HasBigEndian = false;
  ParseSubtargetFeatures(CPU, /*TuneCPU*/ CPU, FS);
  return *this;
}

{{ Xpu }}Subtarget::{{ Xpu }}Subtarget(
  const Triple &TT, StringRef CPU, StringRef FS, const TargetMachine &TM)
    : {{ Xpu }}GenSubtargetInfo(TT, CPU, /*TuneCPU*/ CPU, FS),
      FrameLowering(initializeSubtargetDependencies(CPU, FS)),
      InstrInfo(*this), RegInfo(), TLInfo(TM, *this) {
}
