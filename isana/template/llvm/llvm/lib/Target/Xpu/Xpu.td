//===-- {{ namespace }}.td - Describe the {{ namespace }} Target Machine *- tablegen -*-===//

include "llvm/Target/Target.td"

def Feature64Bit : SubtargetFeature<"64bit", "Has64Bit", "true",
                                    "Enable 64-bit instructions">;
def FeatureBE : SubtargetFeature<"bigendian", "HasBigEndian", "true",
                                 "Enable Big-endian byte order">;
def ProcXPU32le : ProcessorModel<"xpu-32le", NoSchedModel, []>;
def ProcXPU32be : ProcessorModel<"xpu-32be", NoSchedModel, [FeatureBE]>;
def ProcXPU64le : ProcessorModel<"xpu-64le", NoSchedModel, [Feature64Bit]>;
def ProcXPU64be : ProcessorModel<"xpu-64be", NoSchedModel, [Feature64Bit, FeatureBE]>;

include "{{ namespace }}RegisterInfo.td"
include "{{ namespace }}CallingConv.td"
include "{{ namespace }}Schedule.td"
include "{{ namespace }}InstrInfo.td"

def {{ namespace }}InstrInfo : InstrInfo {
}

def {{ namespace }} : Target {
  let InstructionSet = {{ namespace }}InstrInfo;
}
