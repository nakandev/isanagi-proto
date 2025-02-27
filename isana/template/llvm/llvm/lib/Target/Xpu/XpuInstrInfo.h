//===-- {{ Xpu }}InstrInfo.h - {{ Xpu }} Instruction Information -*- C++ -*-===//

#ifndef LLVM_LIB_TARGET_{{ XPU }}_{{ XPU }}INSTRINFO_H
#define LLVM_LIB_TARGET_{{ XPU }}_{{ XPU }}INSTRINFO_H

#include "{{ Xpu }}RegisterInfo.h"
#include "llvm/CodeGen/TargetInstrInfo.h"

#define GET_INSTRINFO_HEADER
#include "{{ Xpu }}GenInstrInfo.inc"

namespace llvm {

class {{ Xpu }}Subtarget;

class {{ Xpu }}InstrInfo : public {{ Xpu }}GenInstrInfo {
public:
  {{ Xpu }}InstrInfo({{ Xpu }}Subtarget &STI);

  bool expandPostRAPseudo(MachineInstr &MI) const override;

  void addImmediate(Register DstReg, Register SrcReg, int64_t Amount,
                    MachineBasicBlock &MBB,
                    MachineBasicBlock::iterator I) const;

  void copyPhysReg(MachineBasicBlock &MBB, MachineBasicBlock::iterator MBBI,
                   const DebugLoc &DL, MCRegister DstReg, MCRegister SrcReg,
                   bool KillSrc, bool RenamableDest = false,
                   bool RenamableSrc = false) const override;

  void storeRegToStackSlot(MachineBasicBlock &MBB,
                           MachineBasicBlock::iterator MBBI, Register SrcReg,
                           bool IsKill, int FrameIndex,
                           const TargetRegisterClass *RC,
                           const TargetRegisterInfo *TRI,
                           Register VReg) const override;

  void loadRegFromStackSlot(MachineBasicBlock &MBB,
                            MachineBasicBlock::iterator MBBI, Register DstReg,
                            int FrameIndex, const TargetRegisterClass *RC,
                            const TargetRegisterInfo *TRI,
                            Register VReg) const override;

protected:
  const {{ Xpu }}Subtarget &STI;

private:
  void expandPseudoRET(MachineBasicBlock &MBB, MachineBasicBlock::iterator I) const;
};
}

#endif
