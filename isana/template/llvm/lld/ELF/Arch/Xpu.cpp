//===- {{ namespace }}.cpp -===//

#include "Symbols.h"
#include "Target.h"
#include "lld/Common/ErrorHandler.h"
#include "llvm/BinaryFormat/ELF.h"
#include "llvm/Support/Endian.h"

using namespace llvm;
using namespace llvm::object;
using namespace llvm::support::endian;
using namespace llvm::ELF;
using namespace lld;
using namespace lld::elf;

namespace {
class {{ namespace }} final : public TargetInfo {
public:
  {{ namespace }}();
  RelExpr getRelExpr(RelType type, const Symbol &s,
                     const uint8_t *loc) const override;
  void relocate(uint8_t *loc, const Relocation &rel,
                uint64_t val) const override;
};
} // namespace

{{ namespace }}::{{ namespace }}() {
}

RelExpr {{ namespace }}::getRelExpr(RelType type, const Symbol &s,
                           const uint8_t *loc) const {
  switch (type) {
  // case R_CUSTOMXPU_PC_REL_0:
  //   return R_PC;
  default:
    return R_ABS;
  }
}

void {{ namespace }}::relocate(uint8_t *loc, const Relocation &rel, uint64_t val) const {
  switch (rel.type) {
  {% for fx in fixup_relocs -%}
  case R_{{ namespace.upper() }}_{{ fx.name.upper() }}: {
    uint32_t newval = read{{ fx.size }}le(loc)
    {% for proc in fx.reloc_procs -%}
    {{ proc }}
    {% endfor -%}
    ;
    write{{ fx.size }}le(loc, newval);
    break; }
  {% endfor %}
  default:
    error(getErrorLocation(loc) + "unrecognized relocation " +
          toString(rel.type));
  }
}

TargetInfo *elf::get{{ namespace }}TargetInfo() {
  static {{ namespace }} target;
  return &target;
}
