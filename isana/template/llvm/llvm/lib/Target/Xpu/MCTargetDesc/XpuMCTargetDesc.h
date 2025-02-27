//===- {{ namespace }}MCTargetDesc.h - {{ namespace }} Target Descriptions -===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}MCTARGETDESC_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_MCTARGETDESC_{{ namespace.upper() }}MCTARGETDESC_H

#include "llvm/MC/MCTargetOptions.h"
#include "llvm/Support/DataTypes.h"
#include <memory>

namespace llvm {
class MCAsmBackend;
class MCCodeEmitter;
class MCContext;
class MCInstrInfo;
class MCObjectTargetWriter;
class MCRegisterInfo;
class MCSubtargetInfo;
class MCTargetOptions;
class StringRef;
class Target;
class Triple;

MCCodeEmitter *create{{ namespace }}MCCodeEmitter(const MCInstrInfo &MCII,
                                            MCContext &Ctx);

MCAsmBackend *create{{ namespace }}AsmBackend(const Target &T, const MCSubtargetInfo &STI,
                                        const MCRegisterInfo &MRI,
                                        const MCTargetOptions &Options);

std::unique_ptr<MCObjectTargetWriter> create{{ namespace }}ELFObjectWriter();
} // namespace llvm

#define GET_REGINFO_ENUM
#include "{{ namespace }}GenRegisterInfo.inc"

// Defines symbolic names for {{ namespace }} instructions.
#define GET_INSTRINFO_ENUM
#define GET_INSTRINFO_MC_HELPER_DECLS
#include "{{ namespace }}GenInstrInfo.inc"

#define GET_SUBTARGETINFO_ENUM
#include "{{ namespace }}GenSubtargetInfo.inc"

#endif

