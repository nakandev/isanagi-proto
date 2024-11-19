from isana.compiler import Fixup
from isana.compiler import LLVMCompiler


class RiscvCompiler(LLVMCompiler):
    namespace = "CustomXPU"
    triple = ("customxpu", "", "")

    def __init__(self, isa):
        super().__init__(isa)


compiler = RiscvCompiler
