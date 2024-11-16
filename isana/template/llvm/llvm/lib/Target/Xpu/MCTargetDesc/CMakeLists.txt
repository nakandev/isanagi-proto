add_llvm_component_library(LLVM{{ namespace }}Desc
  {{ namespace }}AsmBackend.cpp
  # {{ namespace }}BaseInfo.cpp
  {{ namespace }}ELFObjectWriter.cpp
  {{ namespace }}InstPrinter.cpp
  {{ namespace }}MCAsmInfo.cpp
  {{ namespace }}MCCodeEmitter.cpp
  {{ namespace }}MCExpr.cpp
  # {{ namespace }}MCObjectFileInfo.cpp
  {{ namespace }}MCTargetDesc.cpp
  # {{ namespace }}MatInt.cpp
  # {{ namespace }}TargetStreamer.cpp
  # {{ namespace }}ELFStreamer.cpp

  LINK_COMPONENTS
  MC
  {{ namespace }}Info
  Support
  TargetParser

  ADD_TO_COMPONENT
  {{ namespace }}
)
