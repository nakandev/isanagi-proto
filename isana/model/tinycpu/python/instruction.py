from isana.isa import Instruction, parameter, assembly, binary


# bin[ 0: 0] ( 1): instrSize (0:16-bit, 1:32-bit)
# bin[ 3: 1] ( 3): categoryA (0:alu, 1:ldst, 2:branch)
# bin[ 4: 7] ( 4): categoryB
# bin[ 8: *] ( *): depends on categoryA/B
class alui(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR, imm:Imm")
    asm = assembly("$opn $rd, $rs1, $imm")
    bin = binary("$imm[7:0], $rs1[4:0], $rd[4:0], $opc[13:0]")
    # iiiiiiii_sssssddd_ddoooooo_oooooooo


class alu(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR, rs2:GPR")
    asm = assembly("$opn $rd, $rs1, $rs2")
    bin = binary("$opc[16:14], $rs2[4:0], $rs1[4:0], $rd[4:0], $opc[13:0]")
    # oooSSSSS_sssssddd_ddoooooo_oooooooo


class load(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR, imm:Imm")
    asm = assembly("$opn $rd, $imm ($rs1)")
    bin = binary("$imm[7:0], $rs1[4:0], $rd[4:0], $opc[13:0]")
    # iiiiiiii_sssssddd_ddoooooo_oooooooo
    is_load = True


class store(Instruction):
    prm = parameter("", "rd:GPR, rs1:GPR, imm:Imm")
    asm = assembly("$opn $rd, $imm ($rs1)")
    bin = binary("$imm[7:0], $rs1[4:0], $rd[4:0], $opc[13:0]")
    # iiiiiiii_sssssddd_ddoooooo_oooooooo
    is_store = True


class branch(Instruction):
    prm = parameter("rd:GPR", "addr:GPR, imm:Imm")
    asm = assembly("$opn $rd, $imm ($addr)")
    bin = binary("$imm[7:0], $addr[4:0], $rd[4:0], $opc[13:0]")
    # iiiiiiii_sssssddd_ddoooooo_oooooooo


class syscall(Instruction):
    opn, opc = "syscall", 0b00_0000_0000_1111
    prm = parameter("", "imm:Imm")
    asm = assembly("$opn $imm")
    bin = binary("0xff[15:0], $imm[7:0], $opc[7:0]")
    # 00000000_00000000_iiiiiiii_oooooooo


class addi(alui):
    opn, opc = "addi", 0b00000000_00000_00000_000000_0000_000_1

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] + ins.imm


class add(alu):
    opn, opc = "add", 0b000_00000_00101_000000_0001_000_1

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] + ctx.GPR[ins.rs2]


class lw(load):
    opn, opc = "lw", 0b00000000_00000_00000_0000_001_1

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ctx.GPR[ins.rs2]
        ctx.GPR[ins.rd] = ctx.Mem.read(32, addr)


class sw(store):
    opn, opc = "sw", 0b00000000_00000_00000_0001_001_1

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.Mem.write(32, addr, ctx.GPR[ins.rs2])


class jmp(branch):
    opn, opc = "jm", 0b00000000_00000_00000_0000_010_1
    is_jump = True

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.PC.pc + 4
        ctx.PC.pc += ins.imm


class beq(branch):
    opn, opc = "br", 0b00000000_00000_00000_0001_010_1
    is_branch = True

    def semantic(self, ctx, ins):
        cond = ctx.GPR[ins.rs1] == ctx.GPR[ins.rs2]
        if cond:
            ctx.PC.pc += ins.imm


class call(branch):
    opn, opc = "call", 0b00000000_00000_00000_0010_010_1
    is_call = True

    def semantic(self, ctx, ins):
        t = ctx.GPR[ins.rs1]
        ctx.GPR[ins.rd] = ctx.PC.pc + 4
        ctx.PC.pc = t + ins.imm


class ret(branch):
    opn, opc = "ret", 0b00000000_00000_00000_0011_010_1
    is_return = True

    def semantic(self, ctx, ins):
        ctx.PC.pc = ctx.t + ins.imm


instructions = [
    addi,
    add,
    lw,
    sw,
    jmp,
    beq,
    call,
    ret,
]
