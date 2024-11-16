from isana.compiler import Fixup
from isana.compiler import LLVMCompiler


class rel32(Fixup):
    name = "rel32"


class TinyCpuCompiler(LLVMCompiler):
    namespace = "CustomXPU"
    triple = ("customxpu", "", "")

    fixups = (
        # rel32,
    )

    def __init__(self, isa):
        super().__init__(isa)


compiler = TinyCpuCompiler
