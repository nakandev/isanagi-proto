//===- {{ namespace }}InstPrinter.h - Convert {{ namespace }} MCInst to asm syntax -===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}INSTPRINTER_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}INSTPRINTER_H

#include "MCTargetDesc/{{ namespace }}MCTargetDesc.h"
#include "llvm/MC/MCInstPrinter.h"

namespace llvm {

class {{ namespace }}InstPrinter : public MCInstPrinter {
public:
  {{ namespace }}InstPrinter(const MCAsmInfo &MAI, const MCInstrInfo &MII,
                   const MCRegisterInfo &MRI)
      : MCInstPrinter(MAI, MII, MRI) {}

  bool applyTargetSpecificCLOption(StringRef Opt) override;

  void printInst(const MCInst *MI, uint64_t Address, StringRef Annot,
                 const MCSubtargetInfo &STI, raw_ostream &O) override;
  void printRegName(raw_ostream &O, MCRegister Reg) const override;

  void printOperand(const MCInst *MI, unsigned OpNo,
                    raw_ostream &O, const char *Modifier = nullptr);
  void printOperand(const MCInst *MI, unsigned Address, unsigned OpNo,
                    raw_ostream &O, const char *Modifier = nullptr) {
    printOperand(MI, OpNo, O, Modifier);
  }
  {% for asmopcls in asm_operand_clss -%}
  void print{{ asmopcls.name }}(const MCInst *MI, unsigned OpNo,
          raw_ostream &O);
  {% endfor %}
  // Autogenerated by tblgen.
  std::pair<const char *, uint64_t> getMnemonic(const MCInst *MI) override;
  void printInstruction(const MCInst *MI, uint64_t Address,
                        raw_ostream &O);
  bool printAliasInstr(const MCInst *MI, uint64_t Address,
                       raw_ostream &O);
  void printCustomAliasOperand(const MCInst *MI, uint64_t Address,
                               unsigned OpIdx, unsigned PrintMethodIdx,
                               const MCSubtargetInfo &STI, raw_ostream &O);
  static const char *getRegisterName(MCRegister Reg);
};
} // namespace llvm

#endif
