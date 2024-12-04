//===- {{ namespace }}MCExpr.cpp - {{ namespace }} specific MC expression classes -===//

#include "{{ namespace }}FixupKinds.h"
#include "{{ namespace }}MCExpr.h"
#include "llvm/BinaryFormat/ELF.h"
#include "llvm/MC/MCAssembler.h"
#include "llvm/MC/MCContext.h"
#include "llvm/MC/MCStreamer.h"
#include "llvm/MC/MCSymbolELF.h"
#include "llvm/Support/Casting.h"

using namespace llvm;

#define DEBUG_TYPE "{{ namespace.lower() }}-mc-expr"

const {{ namespace }}MCExpr *{{ namespace }}MCExpr::create(const MCExpr *Expr, VariantKind Kind,
                                     MCContext &Ctx) {
  return new (Ctx) {{ namespace }}MCExpr(Kind, Expr);
}

StringRef {{ namespace }}MCExpr::getVariantKindName(VariantKind Kind) {
  switch (Kind) {
  default:
    llvm_unreachable("Invalid ELF symbol kind");
  case VK_{{ namespace }}_None:
    return "";
  case VK_{{ namespace }}_Symbol:
    return "@Sym";
  }
}

void {{ namespace }}MCExpr::visitUsedExpr(MCStreamer &Streamer) const {
  Streamer.visitUsedExpr(*getSubExpr());
}

void {{ namespace }}MCExpr::printImpl(raw_ostream &OS, const MCAsmInfo *MAI) const {
  Expr->print(OS, MAI);
  OS << getVariantKindName(getKind());
}

void {{ namespace }}MCExpr::fixELFSymbolsInTLSFixups(MCAssembler &Asm) const {
  switch (getKind()) {
  default:
    return;
  // case VK_{{ namespace }}_TLSLE:
  // case VK_{{ namespace }}_TLSIE:
  // case VK_{{ namespace }}_TLSGD:
  //   break;
  }

  // fixELFSymbolsInTLSFixupsImpl(getSubExpr(), Asm);
}

bool {{ namespace }}MCExpr::evaluateAsRelocatableImpl(MCValue &Res, const MCAssembler *Asm,
                                           const MCFixup *Fixup) const {
  if (!getSubExpr()->evaluateAsRelocatable(Res, Asm, Fixup))
    return false;

  // Some custom fixup types are not valid with symbol difference expressions
  if (Res.getSymA() && Res.getSymB()) {
    switch (getKind()) {
    default:
      return true;
    // case VK_{{ namespace }}_GOT:
    // case VK_{{ namespace }}_GOTPC:
    // case VK_{{ namespace }}_GOTOFF:
    // case VK_{{ namespace }}_PLT:
    // case VK_{{ namespace }}_TLSIE:
    //   return false;
    }
  }

  return true;
}
