//===-- {{ namespace }}ISelLowering.cpp - {{ namespace }} DAG Lowering Implementation -*- C++ -*-===//

#include "{{ namespace }}ISelLowering.h"
#include "{{ namespace }}.h"
#include "{{ namespace }}Subtarget.h"
#include "{{ namespace }}TargetMachine.h"
#include "llvm/CodeGen/CallingConvLower.h"
#include "llvm/CodeGen/MachineFrameInfo.h"
#include "llvm/CodeGen/MachineFunction.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/CodeGen/MachineRegisterInfo.h"
#include "llvm/CodeGen/TargetLoweringObjectFileImpl.h"
#include "llvm/CodeGen/ValueTypes.h"
#include "llvm/IR/DiagnosticInfo.h"
#include "llvm/IR/DiagnosticPrinter.h"
#include "llvm/Support/Debug.h"
#include "llvm/Support/ErrorHandling.h"
#include "llvm/Support/MathExtras.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

#define DEBUG_TYPE "{{ namespace.lower() }}-lower"

{{ namespace }}TargetLowering::{{ namespace }}TargetLowering(const TargetMachine &TM,
                                                 const {{ namespace }}Subtarget &STI)
    : TargetLowering(TM), Subtarget(STI) {

  MVT XLenVT = Subtarget.getXLenVT();

  // Set up the register classes.
  addRegisterClass(MVT::i32, &{{ namespace }}::GPRRegClass);

  // Compute derived properties from the register classes
  computeRegisterProperties(Subtarget.getRegisterInfo());

  setOperationAction(ISD::BR_JT, MVT::Other, Expand);
  setOperationAction(ISD::BR_CC, XLenVT, Expand);
  // setOperationAction(ISD::BRCOND, MVT::Other, Custom);
  setOperationAction(ISD::SELECT   , XLenVT, Custom);
  setOperationAction(ISD::SELECT_CC, XLenVT, Expand);

  // Function alignments
  setMinFunctionAlignment(Align(4));
  setPrefFunctionAlignment(Align(4));
}

// addLiveIn - This helper function adds the specified physical register to the
// MachineFunction as a live in value.  It also creates a corresponding
// virtual register for it.
static unsigned
addLiveIn(MachineFunction &MF, unsigned PReg, const TargetRegisterClass *RC)
{
  Register VReg = MF.getRegInfo().createVirtualRegister(RC);
  MF.getRegInfo().addLiveIn(PReg, VReg);
  return VReg;
}

// Calling Convention Implementation
#include "{{ namespace }}GenCallingConv.inc"

SDValue
{{ namespace }}TargetLowering::LowerFormalArguments(
  SDValue Chain,
  CallingConv::ID CallConv,
  bool IsVarArg,
  const SmallVectorImpl<ISD::InputArg> &Ins,
  const SDLoc &DL,
  SelectionDAG &DAG,
  SmallVectorImpl<SDValue> &InVals
) const {
  MachineFunction &MF = DAG.getMachineFunction();
  MachineFrameInfo &MFI = MF.getFrameInfo();

  std::vector<SDValue> OutChains;

  SmallVector<CCValAssign, 16> ArgLocs;
  CCState CCInfo(CallConv, IsVarArg, DAG.getMachineFunction(), ArgLocs, *DAG.getContext());
  CCInfo.AnalyzeFormalArguments(Ins, CC_{{ namespace }}32);

  for (unsigned i = 0, e = ArgLocs.size(); i != e; ++i) {
    CCValAssign &VA = ArgLocs[i];
    EVT ValVT = VA.getValVT();
    bool IsRegLoc = VA.isRegLoc();
    if (IsRegLoc) {
      MVT RegVT = VA.getLocVT();
      unsigned ArgReg = VA.getLocReg();
      const TargetRegisterClass *RC = getRegClassFor(RegVT);

      unsigned Reg = addLiveIn(DAG.getMachineFunction(), ArgReg, RC);
      SDValue ArgValue = DAG.getCopyFromReg(Chain, DL, Reg, RegVT);

      if (VA.getLocInfo() != CCValAssign::Full) {
        unsigned Opcode = 0;
        if (VA.getLocInfo() == CCValAssign::SExt)
          Opcode = ISD::AssertSext;
        else if (VA.getLocInfo() == CCValAssign::ZExt)
          Opcode = ISD::AssertZext;
        if (Opcode)
          ArgValue = DAG.getNode(Opcode, DL, RegVT, ArgValue, DAG.getValueType(ValVT));
        ArgValue = DAG.getNode(ISD::TRUNCATE, DL, ValVT, ArgValue);
      }
      InVals.push_back(ArgValue);
    } else {
      MVT LocVT = VA.getLocVT();

      // Only arguments pased on the stack should make it here. 
      assert(VA.isMemLoc());

      int FI = MFI.CreateFixedObject(LocVT.getSizeInBits() / 8,
                                     VA.getLocMemOffset(), true);

      // Create load nodes to retrieve arguments from the stack
      SDValue FIN = DAG.getFrameIndex(FI, getPointerTy(DAG.getDataLayout()));
      SDValue ArgValue = DAG.getLoad(
          LocVT, DL, Chain, FIN,
          MachinePointerInfo::getFixedStack(DAG.getMachineFunction(), FI));
      OutChains.push_back(ArgValue.getValue(1));

      // ArgValue =
      //     UnpackFromArgumentSlot(ArgValue, VA, Ins[InsIdx].ArgVT, DL, DAG);

      InVals.push_back(ArgValue);
    }
  }

  return Chain;
}

SDValue
{{ namespace }}TargetLowering::LowerReturn(
  SDValue Chain,
  CallingConv::ID CallConv,
  bool IsVarArg,
  const SmallVectorImpl<ISD::OutputArg> &Outs,
  const SmallVectorImpl<SDValue> &OutVals,
  const SDLoc &DL,
  SelectionDAG &DAG
) const {
  MachineFunction &MF = DAG.getMachineFunction();
  SmallVector<CCValAssign, 16> RVLocs;

  CCState CCInfo(CallConv, IsVarArg, MF, RVLocs, *DAG.getContext());
  CCInfo.AnalyzeReturn(Outs, RetCC_{{ namespace }}32);

  SDValue Glue;
  SmallVector<SDValue, 4> RetOps(1, Chain);
  for (unsigned i = 0; i != RVLocs.size(); ++i) {
    SDValue Val = OutVals[i];
    CCValAssign &VA = RVLocs[i];
    assert(VA.isRegLoc() && "Can only return in registers!");

    // if (VA.getLocInfo() == CCValAssign::BCvt)
    if (RVLocs[i].getValVT() != RVLocs[i].getLocVT())
      Val = DAG.getNode(ISD::BITCAST, DL, VA.getLocVT(), Val);

    Chain = DAG.getCopyToReg(Chain, DL, VA.getLocReg(), Val, Glue);

    Glue = Chain.getValue(1);
    RetOps.push_back(DAG.getRegister(VA.getLocReg(), VA.getLocVT()));
  }

  RetOps[0] = Chain; // Update chain.

  // Add the glue if we have it.
  if (Glue.getNode())
    RetOps.push_back(Glue);

  return DAG.getNode({{ namespace }}ISD::RET_GLUE, DL, MVT::Other,
                     RetOps);
}

SDValue
{{ namespace }}TargetLowering::LowerCall(
  CallLoweringInfo &CLI,
  SmallVectorImpl<SDValue> &InVals
) const {
  SDValue Chain = CLI.Chain;
  return Chain;
}

SDValue
{{ namespace }}TargetLowering::LowerOperation(
  SDValue Op,
  SelectionDAG &DAG
) const {
  switch (Op.getOpcode()) {
  default:
    report_fatal_error("unimplemented operand");
  case ISD::SELECT:
    return lowerSELECT(Op, DAG);
  }
}

SDValue
{{ namespace }}TargetLowering::lowerSELECT(
  SDValue Op,
  SelectionDAG &DAG
) const {
  SDValue CondV = Op.getOperand(0);
  SDValue TrueV = Op.getOperand(1);
  SDValue FalseV = Op.getOperand(2);
  SDLoc DL(Op);
  MVT VT = Op.getSimpleValueType();
  MVT XLenVT = Subtarget.getXLenVT();

  // (select condv, truev, falsev) -> (SELECT condv, 0, setne, truev, falsev)
  SDValue Zero = DAG.getConstant(0, DL, XLenVT);
  // SDValue SetNE = DAG.getCondCode(ISD::SETNE);
  SDValue SetNE = DAG.getConstant(ISD::SETNE, DL, XLenVT);

  SDValue Ops[] = {CondV, Zero, SetNE, TrueV, FalseV};

  return DAG.getNode({{ namespace }}ISD::SELECT_CC, DL, VT, Ops);
}

const char *
{{ namespace }}TargetLowering::getTargetNodeName(
  unsigned Opcode
) const {
  switch (({{ namespace }}ISD::NodeType)Opcode) {
  case {{ namespace }}ISD::FIRST_NUMBER:
    break;
  case {{ namespace }}ISD::RET_GLUE:
    return "{{ namespace }}ISD::RET_GLUE";
  case {{ namespace }}ISD::CALL:
    return "{{ namespace }}ISD::CALL";
  case {{ namespace }}ISD::SELECT_CC:
    return "{{ namespace }}ISD::SELECT_CC";
  case {{ namespace }}ISD::BR_CC:
    return "{{ namespace }}ISD::BR_CC";
  case {{ namespace }}ISD::Wrapper:
    return "{{ namespace }}ISD::Wrapper";
  case {{ namespace }}ISD::MEMCPY:
    return "{{ namespace }}ISD::MEMCPY";
  }
  return nullptr;
}

static unsigned
getBranchOpcodeForIntCondCode (ISD::CondCode CC) {
  switch (CC) {
  default:
    llvm_unreachable("Unsupported CondCode");
  case ISD::SETEQ:
    return {{ namespace }}::BEQ;
  case ISD::SETNE:
    return {{ namespace }}::BNE;
  case ISD::SETLT:
    return {{ namespace }}::BLT;
  case ISD::SETGE:
    return {{ namespace }}::BGE;
  case ISD::SETULT:
    return {{ namespace }}::BLTU;
  case ISD::SETUGE:
    return {{ namespace }}::BGEU;
  }
}

static MachineBasicBlock *emitSelectPseudo(
  MachineInstr &MI,
  MachineBasicBlock *BB,
  const {{ namespace }}Subtarget &Subtarget
) {
  const TargetInstrInfo &TII = *Subtarget.getInstrInfo();
  const BasicBlock *LLVM_BB = BB->getBasicBlock();
  DebugLoc DL = MI.getDebugLoc();
  MachineFunction::iterator I = ++BB->getIterator();

  MachineBasicBlock *HeadMBB = BB;
  MachineFunction *F = BB->getParent();
  MachineBasicBlock *TailMBB = F->CreateMachineBasicBlock(LLVM_BB);
  MachineBasicBlock *IfFalseMBB = F->CreateMachineBasicBlock(LLVM_BB);

  F->insert(I, IfFalseMBB);
  F->insert(I, TailMBB);

  TailMBB->splice(TailMBB->begin(), HeadMBB,
                  std::next(MachineBasicBlock::iterator(MI)), HeadMBB->end());

  TailMBB->transferSuccessorsAndUpdatePHIs(HeadMBB);
  HeadMBB->addSuccessor(IfFalseMBB);
  HeadMBB->addSuccessor(TailMBB);

  unsigned LHS = MI.getOperand(1).getReg();
  unsigned RHS = MI.getOperand(2).getReg();
  auto CC = static_cast<ISD::CondCode>(MI.getOperand(3).getImm());
  unsigned Opcode = getBranchOpcodeForIntCondCode(CC);

  BuildMI(HeadMBB, DL, TII.get(Opcode))
    .addReg(LHS)
    .addReg(RHS)
    .addMBB(TailMBB);

  IfFalseMBB->addSuccessor(TailMBB);

  // %Result = phi [ %TrueValue, HeadMBB ], [ %FalseValue, IfFalseMBB ]
  BuildMI(*TailMBB, TailMBB->begin(), DL, TII.get({{ namespace }}::PHI),
          MI.getOperand(0).getReg())
      .addReg(MI.getOperand(4).getReg())
      .addMBB(HeadMBB)
      .addReg(MI.getOperand(5).getReg())
      .addMBB(IfFalseMBB);

  MI.eraseFromParent();
  return TailMBB;
}

MachineBasicBlock *
{{ namespace }}TargetLowering::EmitInstrWithCustomInserter(
  MachineInstr &MI,
  MachineBasicBlock *BB
) const {
  switch (MI.getOpcode()) {
  default:
    llvm_unreachable("Unexpected instr type to insert");
  case {{ namespace }}::Select_GPR:
    return emitSelectPseudo(MI, BB, Subtarget);
  }
}
