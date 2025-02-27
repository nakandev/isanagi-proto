add_llvm_component_library(LLVM{{ Xpu }}AsmParser
  {{ Xpu }}AsmParser.cpp

  LINK_COMPONENTS
  {{ Xpu }}Desc
  {{ Xpu }}Info
  MC
  MCParser
  Support
  TargetParser

  ADD_TO_COMPONENT
  {{ Xpu }}
  )
