//===- {{ namespace }}MCAsmInfo.h - {{ namespace }} Asm Info -===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}MCASMINFO_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}MCASMINFO_H

#include "llvm/MC/MCAsmInfoELF.h"

namespace llvm {
class Triple;

class {{ namespace }}MCAsmInfo : public MCAsmInfoELF {
  void anchor() override;

public:
  explicit {{ namespace }}MCAsmInfo(const Triple &TargetTriple);
};

} // namespace llvm

#endif
