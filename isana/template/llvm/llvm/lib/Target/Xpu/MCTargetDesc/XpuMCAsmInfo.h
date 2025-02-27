//===- {{ Xpu }}MCAsmInfo.h - {{ Xpu }} Asm Info -===//

#ifndef LLVM_LIB_TARGET_{{ XPU }}_MCTARGETDESC_{{ XPU }}MCASMINFO_H
#define LLVM_LIB_TARGET_{{ XPU }}_MCTARGETDESC_{{ XPU }}MCASMINFO_H

#include "llvm/MC/MCAsmInfoELF.h"

namespace llvm {
class Triple;

class {{ Xpu }}MCAsmInfo : public MCAsmInfoELF {
  void anchor() override;

public:
  explicit {{ Xpu }}MCAsmInfo(const Triple &TargetTriple);
};

} // namespace llvm

#endif
