add_llvm_component_library(LLVM{{ namespace }}AsmParser
  {{ namespace }}AsmParser.cpp

  LINK_COMPONENTS
  {{ namespace }}Desc
  {{ namespace }}Info
  MC
  MCParser
  Support
  TargetParser

  ADD_TO_COMPONENT
  {{ namespace }}
  )
