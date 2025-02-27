add_llvm_component_library(LLVM{{ Xpu }}Disassembler
  {{ Xpu }}Disassembler.cpp

  LINK_COMPONENTS
  {{ Xpu }}Info
  MCDisassembler
  Support

  ADD_TO_COMPONENT
  {{ Xpu }}
  )
