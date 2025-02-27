add_llvm_component_library(LLVM{{ Xpu }}Desc
  {{ Xpu }}AsmBackend.cpp
  # {{ Xpu }}BaseInfo.cpp
  {{ Xpu }}ELFObjectWriter.cpp
  {{ Xpu }}InstPrinter.cpp
  {{ Xpu }}MCAsmInfo.cpp
  {{ Xpu }}MCCodeEmitter.cpp
  {{ Xpu }}MCExpr.cpp
  # {{ Xpu }}MCObjectFileInfo.cpp
  {{ Xpu }}MCTargetDesc.cpp
  # {{ Xpu }}MatInt.cpp
  # {{ Xpu }}TargetStreamer.cpp
  # {{ Xpu }}ELFStreamer.cpp

  LINK_COMPONENTS
  MC
  {{ Xpu }}Info
  Support
  TargetParser

  ADD_TO_COMPONENT
  {{ Xpu }}
)
