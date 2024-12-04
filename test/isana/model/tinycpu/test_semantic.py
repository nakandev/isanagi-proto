from isana.model.tinycpu.python.isa import isa_le
from isana.semantic import (
    may_change_pc_absolute,
    may_change_pc_relative,
    may_take_memory_address,
)

def test_semantic():
    def semantic_pc_absolute1(self, ctx, ins):
        ctx.PC.pc = ins.imm

    def semantic_pc_absolute2(self, ctx, ins):
        ctx.PC.pc = ins.imm + ins.imm

    def semantic_pc_relative1(self, ctx, ins):
        ctx.PC.pc += ins.imm

    def semantic_pc_relative2(self, ctx, ins):
        ctx.PC.pc = ctx.PC.pc + ins.imm

    def semantic_pc_relative3(self, ctx, ins):
        ctx.PC.pc = ins.imm + ctx.PC.pc

    def semantic_mem_read(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.GPR[ins.rd] = ctx.Mem.read(32, addr)

    def semantic_mem_write(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.Mem.write(32, addr, ctx.GPR[ins.rs2])

    semantics = [
        semantic_pc_absolute1,
        semantic_pc_absolute2,
        semantic_pc_relative1,
        semantic_pc_relative2,
        semantic_pc_relative3,
        semantic_mem_read,
        semantic_mem_write,
    ]
    checkers = [
        may_change_pc_absolute,
        may_change_pc_relative,
        may_take_memory_address,
    ]
    for semantic in semantics:
        ress = []
        for checker in checkers:
            res = checker(semantic)
            ress.append(res)
        print(semantic.__name__, ress)

    isa = isa_le
    for instr in isa.instructions:
        ress = []
        for checker in checkers:
            res = checker(instr.semantic)
            ress.append(res)
        print(instr.opn, ress)


if __name__ == '__main__':
    test_semantic()
