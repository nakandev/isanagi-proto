//===- {{ Xpu }}TargetInfo.cpp - {{ Xpu }} Target Implementation -===//

#include "TargetInfo/{{ Xpu }}TargetInfo.h"
#include "llvm/MC/TargetRegistry.h"
using namespace llvm;

Target &llvm::getThe{{ Xpu }}32leTarget() {
  static Target The{{ Xpu }}32leTarget;
  return The{{ Xpu }}32leTarget;
}

Target &llvm::getThe{{ Xpu }}32beTarget() {
  static Target The{{ Xpu }}32beTarget;
  return The{{ Xpu }}32beTarget;
}

Target &llvm::getThe{{ Xpu }}64leTarget() {
  static Target The{{ Xpu }}64leTarget;
  return The{{ Xpu }}64leTarget;
}

Target &llvm::getThe{{ Xpu }}64beTarget() {
  static Target The{{ Xpu }}64beTarget;
  return The{{ Xpu }}64beTarget;
}

extern "C" LLVM_EXTERNAL_VISIBILITY void LLVMInitialize{{ Xpu }}TargetInfo() {
  RegisterTarget<Triple::{{ xpu }}32le, /*HasJIT=*/true> Z(
      getThe{{ Xpu }}32leTarget(), "{{ xpu }}32le", "{{ Xpu }} 32-bit (little endian)", "{{ Xpu }}");
  RegisterTarget<Triple::{{ xpu }}32be, /*HasJIT=*/true> Y(
      getThe{{ Xpu }}32beTarget(), "{{ xpu }}32be", "{{ Xpu }} 32-bit (big endian)", "{{ Xpu }}");
  RegisterTarget<Triple::{{ xpu }}64le, /*HasJIT=*/true> X(
      getThe{{ Xpu }}64leTarget(), "{{ xpu }}64le", "{{ Xpu }} 64-bit (little endian)", "{{ Xpu }}");
  RegisterTarget<Triple::{{ xpu }}64be, /*HasJIT=*/true> W(
      getThe{{ Xpu }}64beTarget(), "{{ xpu }}64be", "{{ Xpu }} 64-bit (big endian)", "{{ Xpu }}");
}
