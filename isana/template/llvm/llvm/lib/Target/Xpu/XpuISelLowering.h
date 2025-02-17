//===-- {{ namespace }}ISelLowering.h - {{ namespace }} DAG Lowering Interface -*- C++ -*-===//

#ifndef LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}ISELLOWERING_H
#define LLVM_LIB_TARGET_{{ namespace.upper() }}_{{ namespace.upper() }}ISELLOWERING_H

#include "{{ namespace }}.h"
#include "llvm/CodeGen/SelectionDAG.h"
#include "llvm/CodeGen/TargetLowering.h"

namespace llvm {
class {{ namespace }}Subtarget;
namespace {{ namespace }}ISD {
enum NodeType : unsigned {
  FIRST_NUMBER = ISD::BUILTIN_OP_END,
  RET_GLUE,
  CALL,
  SELECT_CC,
  BR_CC,
  Wrapper,
  MEMCPY
};
}

class {{ namespace }}TargetLowering : public TargetLowering {
  const {{ namespace }}Subtarget &Subtarget;
public:
  explicit {{ namespace }}TargetLowering(const TargetMachine &TM, const {{ namespace }}Subtarget &STI);

  // Lower incoming arguments, copy physregs into vregs
  SDValue LowerFormalArguments(SDValue Chain, CallingConv::ID CallConv,
                               bool IsVarArg,
                               const SmallVectorImpl<ISD::InputArg> &Ins,
                               const SDLoc &DL, SelectionDAG &DAG,
                               SmallVectorImpl<SDValue> &InVals) const override;

  SDValue LowerReturn(SDValue Chain, CallingConv::ID CallConv, bool IsVarArg,
                      const SmallVectorImpl<ISD::OutputArg> &Outs,
                      const SmallVectorImpl<SDValue> &OutVals, const SDLoc &DL,
                      SelectionDAG &DAG) const override;

  // Provide custom lowering hooks for some operations.
  SDValue LowerOperation(SDValue Op, SelectionDAG &DAG) const override;

  // This method returns the name of a target specific DAG node.
  const char *getTargetNodeName(unsigned Opcode) const override;

  MachineBasicBlock *
  EmitInstrWithCustomInserter(MachineInstr &MI,
                              MachineBasicBlock *BB) const override;

private:
  // Control Instruction Selection Features
  // SDValue LowerGlobalAddress(SDValue Op, SelectionDAG &DAG) const;

  SDValue LowerCall(TargetLowering::CallLoweringInfo &CLI,
                    SmallVectorImpl<SDValue> &InVals) const override;

  SDValue lowerSELECT(SDValue Op, SelectionDAG &DAG) const;
};
}

#endif
