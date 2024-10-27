from isana.compiler import Relocation
from isana.compiler import LLVMCompiler


class REL32(Relocation):
    pass


class TinyCpuCompiler(LLVMCompiler):
    namespace = "CustomXPU"
    triple = ("customxpu", "", "")

    def __init__(self, isa):
        super().__init__(isa)


compiler = TinyCpuCompiler
