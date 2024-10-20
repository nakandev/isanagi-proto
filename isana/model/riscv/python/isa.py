from isana.isa import ISA
from isana.isa import Context
# from isana.isa import signed
# from isana.isa import unimpl

from .memory import Mem
from .register import GPR, GPRC, CSR, PCR
from .datatype import Imm, ImmS12, ImmS13, ImmS21, ImmHi20, ImmS6, ImmS9

from .instruction import instructions


class RiscvContext(Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def pre_semantic(self):
        self.PCR.prev_pc = self.PCR.pc

    def post_semantic(self, ins):
        is_jump = any([
            ins.is_jump, ins.is_branch, ins.is_call, ins.is_tail, ins.is_return
        ])
        if not is_jump:
            self.PCR.pc = self.PCR.pc + 4


class RiscvISA(ISA):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


isa = RiscvISA(
    name="riscv",
    registers=(
        GPR,
        GPRC,
        PCR,
        CSR,
    ),
    memories=(
        Mem,
    ),
    immediates=(
        Imm,
        ImmS12,
        ImmS13,
        ImmS21,
        ImmHi20,
        ImmS6,
        ImmS9,
    ),
    instructions=tuple(instructions),
    context=RiscvContext,
)
