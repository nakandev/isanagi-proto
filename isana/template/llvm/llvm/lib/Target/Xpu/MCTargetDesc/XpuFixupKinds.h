//===- {{ Xpu }}FixupKinds.h - {{ Xpu }} Specific Fixup Entries -===//

#ifndef LLVM_LIB_TARGET_{{ XPU }}_MCTARGETDESC_{{ XPU }}FIXUPKINDS_H
#define LLVM_LIB_TARGET_{{ XPU }}_MCTARGETDESC_{{ XPU }}FIXUPKINDS_H

#include "llvm/MC/MCFixup.h"

namespace llvm {
namespace {{ Xpu }} {
enum Fixups {
  {% for fx in fixups -%}
  {{ fx.name_enum }}{% if loop.first %} = FirstTargetFixupKind{% endif %},
  {% endfor -%}
  // Marker
  fixup_{{ xpu }}_invalid,
  NumTargetFixupKinds = fixup_{{ xpu }}_invalid - FirstTargetFixupKind
};
} // end namespace {{ Xpu }}
} // end namespace llvm

#endif // LLVM_LIB_TARGET_{{ XPU }}_MCTARGETDESC_{{ XPU }}FIXUPKINDS_H
