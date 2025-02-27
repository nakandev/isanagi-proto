add_llvm_component_library(LLVM{{ namespace }}Info
  {{ namespace }}TargetInfo.cpp

  LINK_COMPONENTS
  MC
  Support

  ADD_TO_COMPONENT
  {{ namespace }}
)
