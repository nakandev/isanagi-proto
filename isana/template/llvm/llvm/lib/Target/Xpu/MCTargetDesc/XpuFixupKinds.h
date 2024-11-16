//===- {{ namespace }}FixupKinds.h - {{ namespace }} Specific Fixup Entries -===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}FIXUPKINDS_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}FIXUPKINDS_H

#include "llvm/MC/MCFixup.h"

namespace llvm {
namespace {{ namespace }} {
enum Fixups {
  {% for fx in fixups -%}
  {{ fx.name_enum }}{% if loop.first %} = FirstTargetFixupKind{% endif %},
  {% endfor -%}
  // Marker
  fixup_{{ namespace.lower() }}_invalid,
  NumTargetFixupKinds = fixup_{{ namespace.lower() }}_invalid - FirstTargetFixupKind
};
} // end namespace {{ namespace }}
} // end namespace llvm

#endif // LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}FIXUPKINDS_H
