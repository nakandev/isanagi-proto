//===- {{ namespace }}TargetInfo.h - {{ namespace }} Target Implementation -===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_TARGETINFO_{{ namespace.upper() }}TARGETINFO_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_TARGETINFO_{{ namespace.upper() }}TARGETINFO_H

namespace llvm {

class Target;

Target &getThe{{ namespace }}32leTarget();
Target &getThe{{ namespace }}32beTarget();
Target &getThe{{ namespace }}64leTarget();
Target &getThe{{ namespace }}64beTarget();

} // namespace llvm

#endif // LLVM_LIB_TARGET_{{ namespace.upper() }}_TARGETINFO_{{ namespace.upper() }}TARGETINFO_H

