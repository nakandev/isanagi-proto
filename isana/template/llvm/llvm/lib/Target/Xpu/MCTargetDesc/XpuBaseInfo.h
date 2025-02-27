//===- {{ namespace }}BaseInfo.h - Top level definitions for {{ namespace }} MC -===//
//
// This file contains small standalone enum definitions for the {{ namespace }} target
// useful for the compiler back-end and the MC libraries.
//
//===----------------------------------------------------------------------===//
#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}BASEINFO_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}BASEINFO_H

#include "MCTargetDesc/{{ namespace }}MCTargetDesc.h"
#include "llvm/ADT/APFloat.h"
#include "llvm/ADT/APInt.h"
#include "llvm/ADT/StringRef.h"
#include "llvm/ADT/StringSwitch.h"
#include "llvm/MC/MCInstrDesc.h"

namespace llvm {

// {{ namespace }}II - This namespace holds all of the target specific flags that
// instruction info tracks.
namespace {{ namespace }}II {
// {{ namespace }} Specific Machine Operand Flags
enum {
  MO_None = 0,
  MO_CALL = 1,
};
} // namespace {{ namespace }}II

} // namespace llvm

#endif // LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}BASEINFO_H

