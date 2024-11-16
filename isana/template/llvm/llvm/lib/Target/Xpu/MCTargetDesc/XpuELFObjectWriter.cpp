//===- {{ namespace }}ELFObjectWriter.cpp - {{ namespace }} ELF Writer -===//

#include "{{ namespace }}FixupKinds.h"
#include "{{ namespace }}MCExpr.h"
#include "{{ namespace }}MCTargetDesc.h"
#include "llvm/MC/MCContext.h"
#include "llvm/MC/MCELFObjectWriter.h"
#include "llvm/MC/MCObjectWriter.h"
// #include "llvm/MC/MCSymbol.h"
#include "llvm/MC/MCValue.h"

#define DEBUG_TYPE "{{ namespace.lower() }}-elf-object-writer"

using namespace llvm;

namespace {

class {{ namespace }}ELFObjectWriter : public MCELFObjectTargetWriter {
public:
  {{ namespace }}ELFObjectWriter(uint8_t OSABI = 0)
      : MCELFObjectTargetWriter(false, OSABI, ELF::EM_{{ namespace.upper() }}, true){};
  ~{{ namespace }}ELFObjectWriter() {}

  unsigned getRelocType(MCContext &Ctx, const MCValue &Target,
                        const MCFixup &Fixup, bool IsPCRel) const override;
};

} // namespace

unsigned
{{ namespace }}ELFObjectWriter::getRelocType(
  MCContext &Ctx,
  const MCValue &Target,
  const MCFixup &Fixup,
  bool IsPCRel
) const
{
  const MCExpr *Expr = Fixup.getValue();
  // Determine the type of the relocation
  unsigned Kind = Fixup.getTargetKind();
  // MCSymbolRefExpr::VariantKind Modifier = Target.getAccessVariant();

  if (IsPCRel) {
    switch (Kind) {
    default:
      LLVM_DEBUG(dbgs() << "Unknown Kind1  = " << Kind);
      Ctx.reportError(Fixup.getLoc(), "Unsupported relocation type");
      return ELF::R_CKCORE_NONE;
    case FK_PCRel_4:
      return ELF::R_CKCORE_PCREL32;
    {% for fx in fixups_pc_rel -%}
    case {{ namespace }}::{{ fx.name_enum }}:
      return ELF::R_{{ namespace.upper() }}_{{ fx.name.upper() }};
    {% endfor %}
    }
  }

  switch (Kind) {
  default:
    LLVM_DEBUG(dbgs() << "Unknown Kind2  = " << Kind);
    Ctx.reportError(Fixup.getLoc(), "Unsupported relocation type");
    return ELF::R_CKCORE_NONE;
  case FK_Data_1:
    Ctx.reportError(Fixup.getLoc(), "1-byte data relocations not supported");
    return ELF::R_CKCORE_NONE;
  case FK_Data_2:
    Ctx.reportError(Fixup.getLoc(), "2-byte data relocations not supported");
    return ELF::R_CKCORE_NONE;
  case FK_Data_4:
    if (Expr->getKind() == MCExpr::Target) {
      auto TK = cast<{{ namespace }}MCExpr>(Expr)->getKind();
      // if (TK == {{ namespace }}MCExpr::VK_{{ namespace }}_ADDR)
      //   return ELF::R_CKCORE_ADDR32;
      if (TK == {{ namespace }}MCExpr::VK_{{ namespace }}_None)
        return ELF::R_CKCORE_ADDR32;
      return ELF::R_{{ namespace.upper() }}_32;
    }
    // else {
    //   switch (Modifier) {
    //   default:
    //     Ctx.reportError(Fixup.getLoc(),
    //                     "invalid fixup for 4-byte data relocation");
    //     return ELF::R_CKCORE_NONE;
    //   case MCSymbolRefExpr::VK_None:
    //     return ELF::R_CKCORE_ADDR32;
    //   }
    // }
    // return ELF::R_CKCORE_NONE;
    return ELF::R_{{ namespace.upper() }}_32;
  case FK_Data_8:
    return ELF::R_{{ namespace.upper() }}_64;
  {% for fx in fixup_relocs -%}
  case {{ namespace }}::{{ fx.name_enum }}:
    return ELF::R_{{ namespace.upper() }}_{{ fx.name.upper() }};
  {% endfor %}
  }
}

std::unique_ptr<MCObjectTargetWriter>
llvm::create{{ namespace }}ELFObjectWriter(
)
{
  return std::make_unique<{{ namespace }}ELFObjectWriter>();
}
