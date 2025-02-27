//===- {{ namespace }}TargetInfo.cpp - {{ namespace }} Target Implementation -===//

#include "TargetInfo/{{ namespace }}TargetInfo.h"
#include "llvm/MC/TargetRegistry.h"
using namespace llvm;

Target &llvm::getThe{{ namespace }}32leTarget() {
  static Target The{{ namespace }}32leTarget;
  return The{{ namespace }}32leTarget;
}

Target &llvm::getThe{{ namespace }}32beTarget() {
  static Target The{{ namespace }}32beTarget;
  return The{{ namespace }}32beTarget;
}

Target &llvm::getThe{{ namespace }}64leTarget() {
  static Target The{{ namespace }}64leTarget;
  return The{{ namespace }}64leTarget;
}

Target &llvm::getThe{{ namespace }}64beTarget() {
  static Target The{{ namespace }}64beTarget;
  return The{{ namespace }}64beTarget;
}

extern "C" LLVM_EXTERNAL_VISIBILITY void LLVMInitialize{{ namespace }}TargetInfo() {
  RegisterTarget<Triple::{{ namespace.lower() }}32le, /*HasJIT=*/true> Z(
      getThe{{ namespace }}32leTarget(), "{{ namespace.lower() }}32le", "{{ namespace }} 32-bit (little endian)", "{{ namespace }}");
  RegisterTarget<Triple::{{ namespace.lower() }}32be, /*HasJIT=*/true> Y(
      getThe{{ namespace }}32beTarget(), "{{ namespace.lower() }}32be", "{{ namespace }} 32-bit (big endian)", "{{ namespace }}");
  RegisterTarget<Triple::{{ namespace.lower() }}64le, /*HasJIT=*/true> X(
      getThe{{ namespace }}64leTarget(), "{{ namespace.lower() }}64le", "{{ namespace }} 64-bit (little endian)", "{{ namespace }}");
  RegisterTarget<Triple::{{ namespace.lower() }}64be, /*HasJIT=*/true> W(
      getThe{{ namespace }}64beTarget(), "{{ namespace.lower() }}64be", "{{ namespace }} 64-bit (big endian)", "{{ namespace }}");
}
