def p3_stage0_fe(ctx, fifo):
    pc_next, = fifo
    pc = pc_next
    ins_bin = ctx.IMem.read(pc, 4)
    return (pc, ins_bin)


def p3_stage1_de(ctx, fifo):
    pc, ins_bin = fifo
    ins = ctx.hwdecode(ins_bin)
    return (pc, ins)


def p3_stage2_ex(ctx, fifo):
    pc, ins = fifo
    if ins.opc in ctx.ALU:
        dst = ctx.ALU(ctx.GPR[ins.rs1], ctx.GPR[ins.rs2])
        ctx.GPR[ins.rs1] = dst
    elif ins.opc in ctx.ST:
        pass
    elif ins.opc in ctx.LD:
        pass
    elif ins.opc in ctx.BRANCH:
        pass
    elif ins.opc in ctx.CALL:
        pass
