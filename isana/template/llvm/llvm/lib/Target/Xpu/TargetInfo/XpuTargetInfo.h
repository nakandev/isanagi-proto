//===- {{ Xpu }}TargetInfo.h - {{ Xpu }} Target Implementation -===//

#ifndef LLVM_LIB_TARGET_{{ XPU }}_TARGETINFO_{{ XPU }}TARGETINFO_H
#define LLVM_LIB_TARGET_{{ XPU }}_TARGETINFO_{{ XPU }}TARGETINFO_H

namespace llvm {

class Target;

Target &getThe{{ Xpu }}32leTarget();
Target &getThe{{ Xpu }}32beTarget();
Target &getThe{{ Xpu }}64leTarget();
Target &getThe{{ Xpu }}64beTarget();

} // namespace llvm

#endif // LLVM_LIB_TARGET_{{ XPU }}_TARGETINFO_{{ XPU }}TARGETINFO_H

