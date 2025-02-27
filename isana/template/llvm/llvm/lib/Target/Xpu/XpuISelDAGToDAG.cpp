//===-- {{ Xpu }}ISelDAGToDAG.cpp - A Dag to Dag Inst Selector for {{ Xpu }} -*- C++ -*-===//

#include "{{ Xpu }}ISelDAGToDAG.h"
// #include "MCTargetDesc/{{ Xpu }}BaseInfo.h"
#include "{{ Xpu }}.h"
// #include "{{ Xpu }}MachineFunction.h"
#include "{{ Xpu }}RegisterInfo.h"
#include "llvm/CodeGen/MachineConstantPool.h"
#include "llvm/CodeGen/MachineFrameInfo.h"
#include "llvm/CodeGen/MachineFunction.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"
#include "llvm/CodeGen/MachineRegisterInfo.h"
#include "llvm/CodeGen/SelectionDAG.h"
#include "llvm/CodeGen/SelectionDAGNodes.h"
#include "llvm/CodeGen/StackProtector.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/GlobalValue.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Intrinsics.h"
#include "llvm/IR/Type.h"
#include "llvm/Support/Debug.h"
#include "llvm/Support/ErrorHandling.h"
#include "llvm/Support/KnownBits.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Target/TargetMachine.h"
using namespace llvm;

#define DEBUG_TYPE "{{ xpu }}-isel"
#define PASS_NAME "{{ Xpu }} DAG->DAG Pattern Instruction Selection"

//===----------------------------------------------------------------------===//
// Instruction Selector Implementation
//===----------------------------------------------------------------------===//

//===----------------------------------------------------------------------===//
// {{ Xpu }}DAGToDAGISel - {{ Xpu }} specific code to select {{ Xpu }} machine
// instructions for SelectionDAG operations.
//===----------------------------------------------------------------------===//

bool {{ Xpu }}DAGToDAGISel::runOnMachineFunction(MachineFunction &MF) {
  Subtarget = &MF.getSubtarget<{{ Xpu }}Subtarget>();
  bool Ret = SelectionDAGISel::runOnMachineFunction(MF);

  // processFunctionAfterISel(MF);

  return Ret;
}

bool {{ Xpu }}DAGToDAGISel::SelectAddrFrameIndex(
  SDValue Addr,
  SDValue &Base
) {
  auto VT = MVT::i32;
  SDLoc DL(Addr);

  if (auto *FIN = dyn_cast<FrameIndexSDNode>(Addr)) {
    Base = CurDAG->getTargetFrameIndex(FIN->getIndex(), VT);
    return true;
  }

  return false;
}

bool {{ Xpu }}DAGToDAGISel::SelectAddrFrameIndexRegImm(
  SDValue Addr,
  SDValue &Base,
  SDValue &Offset
) {
  auto VT = MVT::i32;
  SDLoc DL(Addr);

  // (frameindex) -> (frameindex, 0)
  if (SelectAddrFrameIndex(Addr, Base)) {
    Offset = CurDAG->getTargetConstant(0, DL, VT);
    return true;
  }

  if (CurDAG->isBaseWithConstantOffset(Addr)) {
    // (add frameindex, imm) -> (frameindex, imm)
    if (auto *FIN = dyn_cast<FrameIndexSDNode>(Addr.getOperand(0))) {
      int64_t CVal = cast<ConstantSDNode>(Addr.getOperand(1))->getSExtValue();
      Base = CurDAG->getTargetFrameIndex(FIN->getIndex(), VT);
      Offset = CurDAG->getSignedConstant(CVal, DL, VT, /*isTarget=*/true);
      return true;
    }
  }

  return false;
}

bool {{ Xpu }}DAGToDAGISel::SelectAddrGlobal(
  SDValue Addr,
  SDValue &Base
) {
  SDLoc DL(Addr);

  if (auto *GA = dyn_cast<GlobalAddressSDNode>(Addr)) {
    Base = CurDAG->getTargetGlobalAddress(GA->getGlobal(), DL,
                                          /*getPointerTy(CurDAG->getDataLayout())*/
                                          Addr.getValueType());
    return true;
  }

  return false;
}

bool {{ Xpu }}DAGToDAGISel::SelectAddrGlobalRegImm(
  SDValue Addr,
  SDValue &Base,
  SDValue &Offset
) {
  auto VT = MVT::i32;
  SDLoc DL(Addr);

  // (globaladdr) -> (globaladdr, 0)
  if (SelectAddrGlobal(Addr, Base)) {
    Offset = CurDAG->getTargetConstant(0, DL, VT);
    return true;
  }

  if (CurDAG->isBaseWithConstantOffset(Addr)) {
    // (add (globaladdr), imm) -> (globaladdr, imm)
    if (auto *GA = dyn_cast<GlobalAddressSDNode>(Addr.getOperand(0))) {
      int64_t CVal = cast<ConstantSDNode>(Addr.getOperand(1))->getSExtValue();
      Base = CurDAG->getTargetGlobalAddress(GA->getGlobal(), DL,
                                          /*getPointerTy(CurDAG->getDataLayout())*/
                                          Addr.getValueType());
      Offset = CurDAG->getTargetConstant(0, DL, VT);
      return true;
    }
  }

  return false;
}

bool {{ Xpu }}DAGToDAGISel::SelectAddrRegImm(
  SDValue Addr,
  SDValue &Base,
  SDValue &Offset
) {
  auto VT = MVT::i32;
  SDLoc DL(Addr);

  if (SelectAddrFrameIndexRegImm(Addr, Base, Offset)) {
    return true;
  }

  if (SelectAddrGlobalRegImm(Addr, Base, Offset)) {
    return true;
  }

  if (CurDAG->isBaseWithConstantOffset(Addr)) {
    // (add addr, imm) -> (addr, imm)
    Base = Addr.getOperand(0);
    int64_t CVal = cast<ConstantSDNode>(Addr.getOperand(1))->getSExtValue();
    Offset = CurDAG->getTargetConstant(CVal, DL, VT);
    return true;
  }

    // (imm) -> (zero, imm)
  if (auto *CVal = dyn_cast<ConstantSDNode>(Addr)) {
    Base = CurDAG->getRegister(CustomXPU::X0, VT);
    Offset = Addr;
    return true;
  }

  Base = Addr;
  Offset = CurDAG->getTargetConstant(0, DL, VT);
  return true;
}

/// Select instructions not customized! Used for
/// expanded, promoted and normal instructions
void {{ Xpu }}DAGToDAGISel::Select(SDNode *Node) {
  // unsigned Opcode = Node->getOpcode();

  // If we have a custom node, we already have selected!
  if (Node->isMachineOpcode()) {
    LLVM_DEBUG(errs() << "== "; Node->dump(CurDAG); errs() << "\n");
    Node->setNodeId(-1);
    return;
  }

  // See if subclasses can handle this node.
  // if (trySelect(Node))
  //   return;

  // Select the default instruction
  SelectCode(Node);
}

bool {{ Xpu }}DAGToDAGISel::SelectInlineAsmMemoryOperand(
    const SDValue &Op, InlineAsm::ConstraintCode ConstraintID,
    std::vector<SDValue> &OutOps) {
  // All memory constraints can at least accept raw pointers.
  switch(ConstraintID) {
  default:
    llvm_unreachable("Unexpected asm memory constraint");
  case InlineAsm::ConstraintCode::m:
  case InlineAsm::ConstraintCode::R:
  case InlineAsm::ConstraintCode::ZC:
    OutOps.push_back(Op);
    return false;
  }
  return true;
}

char {{ Xpu }}DAGToDAGISelLegacy::ID = 0;

{{ Xpu }}DAGToDAGISelLegacy::{{ Xpu }}DAGToDAGISelLegacy(
    {{ Xpu }}TargetMachine &TM, CodeGenOptLevel OptLevel)
      : SelectionDAGISelLegacy(
            ID, std::make_unique<{{ Xpu }}DAGToDAGISel>(TM, OptLevel)) {}

INITIALIZE_PASS({{ Xpu }}DAGToDAGISelLegacy, DEBUG_TYPE, PASS_NAME, false, false)

FunctionPass *llvm::create{{ Xpu }}ISelDag({{ Xpu }}TargetMachine &TM,
                                           CodeGenOptLevel OptLevel) {
  return new {{ Xpu }}DAGToDAGISelLegacy(TM, OptLevel);
}
