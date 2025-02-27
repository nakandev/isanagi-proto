//===- {{ Xpu }}MCTargetDesc.h - {{ Xpu }} Target Descriptions -===//

#ifndef LLVM_LIB_TARGET_{{ XPU }}_MCTARGETDESC_{{ XPU }}MCTARGETDESC_H
#define LLVM_LIB_TARGET_{{ XPU }}_MCTARGETDESC_{{ XPU }}MCTARGETDESC_H

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

MCCodeEmitter *create{{ Xpu }}MCCodeEmitter(const MCInstrInfo &MCII,
                                            MCContext &Ctx);

MCAsmBackend *create{{ Xpu }}AsmBackend(const Target &T, const MCSubtargetInfo &STI,
                                        const MCRegisterInfo &MRI,
                                        const MCTargetOptions &Options);

std::unique_ptr<MCObjectTargetWriter> create{{ Xpu }}ELFObjectWriter();
} // namespace llvm

#define GET_REGINFO_ENUM
#include "{{ Xpu }}GenRegisterInfo.inc"

// Defines symbolic names for {{ Xpu }} instructions.
#define GET_INSTRINFO_ENUM
#define GET_INSTRINFO_MC_HELPER_DECLS
#include "{{ Xpu }}GenInstrInfo.inc"

#define GET_SUBTARGETINFO_ENUM
#include "{{ Xpu }}GenSubtargetInfo.inc"

#endif

