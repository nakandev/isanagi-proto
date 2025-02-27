add_llvm_component_group({{ namespace }})

set(LLVM_TARGET_DEFINITIONS {{ namespace }}.td)

tablegen(LLVM {{ namespace }}GenAsmMatcher.inc -gen-asm-matcher)
tablegen(LLVM {{ namespace }}GenAsmWriter.inc -gen-asm-writer)
tablegen(LLVM {{ namespace }}GenCallingConv.inc -gen-callingconv)
tablegen(LLVM {{ namespace }}GenDAGISel.inc -gen-dag-isel)
tablegen(LLVM {{ namespace }}GenDisassemblerTables.inc -gen-disassembler)
# tablegen(LLVM {{ namespace }}GenGlobalISel.inc -gen-global-isel)
# tablegen(LLVM {{ namespace }}GenPreLegalizeGICombiner.inc -gen-global-isel-combiner
#               -combiners="{{ namespace }}PreLegalizerCombiner")
# tablegen(LLVM {{ namespace }}GenPostLegalizeGICombiner.inc -gen-global-isel-combiner
#               -combiners="{{ namespace }}PostLegalizerCombiner")
tablegen(LLVM {{ namespace }}GenInstrInfo.inc -gen-instr-info)
tablegen(LLVM {{ namespace }}GenMCCodeEmitter.inc -gen-emitter)
tablegen(LLVM {{ namespace }}GenMCPseudoLowering.inc -gen-pseudo-lowering)
# tablegen(LLVM {{ namespace }}GenRegisterBank.inc -gen-register-bank)
tablegen(LLVM {{ namespace }}GenRegisterInfo.inc -gen-register-info)
# tablegen(LLVM {{ namespace }}GenSearchableTables.inc -gen-searchable-tables)
tablegen(LLVM {{ namespace }}GenSubtargetInfo.inc -gen-subtarget)

add_public_tablegen_target({{ namespace }}CommonTableGen)

add_llvm_target({{ namespace }}CodeGen
  {{ namespace }}AsmPrinter.cpp
  # {{ namespace }}CodeGenPrepare.cpp
  # {{ namespace }}DeadRegisterDefinitions.cpp
  # {{ namespace }}MakeCompressible.cpp
  # {{ namespace }}ExpandAtomicPseudoInsts.cpp
  # {{ namespace }}ExpandPseudoInsts.cpp
  {{ namespace }}FrameLowering.cpp
  # {{ namespace }}GatherScatterLowering.cpp
  # {{ namespace }}IndirectBranchTracking.cpp
  # {{ namespace }}InsertVSETVLI.cpp
  # {{ namespace }}InsertReadWriteCSR.cpp
  # {{ namespace }}InsertWriteVXRM.cpp
  {{ namespace }}InstrInfo.cpp
  {{ namespace }}ISelDAGToDAG.cpp
  {{ namespace }}ISelLowering.cpp
  # {{ namespace }}LandingPadSetup.cpp
  # {{ namespace }}MachineFunctionInfo.cpp
  # {{ namespace }}MergeBaseOffset.cpp
  # {{ namespace }}OptWInstrs.cpp
  # {{ namespace }}PostRAExpandPseudoInsts.cpp
  # {{ namespace }}RedundantCopyElimination.cpp
  # {{ namespace }}MoveMerger.cpp
  # {{ namespace }}PushPopOptimizer.cpp
  {{ namespace }}RegisterInfo.cpp
  {{ namespace }}Subtarget.cpp
  {{ namespace }}TargetMachine.cpp
  # {{ namespace }}TargetObjectFile.cpp
  # {{ namespace }}TargetTransformInfo.cpp
  # {{ namespace }}VectorPeephole.cpp
  # GISel/{{ namespace }}CallLowering.cpp
  # GISel/{{ namespace }}InstructionSelector.cpp
  # GISel/{{ namespace }}LegalizerInfo.cpp
  # GISel/{{ namespace }}PostLegalizerCombiner.cpp
  # GISel/{{ namespace }}O0PreLegalizerCombiner.cpp
  # GISel/{{ namespace }}PreLegalizerCombiner.cpp
  # GISel/{{ namespace }}RegisterBankInfo.cpp

  LINK_COMPONENTS
  Analysis
  AsmPrinter
  CodeGen
  CodeGenTypes
  Core
  GlobalISel
  IPO
  MC
  {{ namespace }}Desc
  {{ namespace }}Info
  Scalar
  SelectionDAG
  Support
  Target
  TargetParser
  TransformUtils
  Vectorize

  ADD_TO_COMPONENT
  {{ namespace }}
  )

add_subdirectory(AsmParser)
add_subdirectory(Disassembler)
add_subdirectory(MCTargetDesc)
add_subdirectory(TargetInfo)

