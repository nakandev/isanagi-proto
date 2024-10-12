from isana.isa import RegisterGroup, Register

PC = RegisterGroup("PC", width=32, regs=(
    Register(0, "pc"),
    Register(1, "prev_pc"),
))

GPR = RegisterGroup("GPR", width=32, regs=(
    Register(0, "x0", "zero"),
    Register(1, "x1", "ra"),
    Register(2, "x2", "sp"),
    Register(3, "x3", "t0"),
    Register(4, "x3", "t1"),
    Register(5, "x3", "s0"),
    Register(6, "x3", "s1"),
    Register(7, "x3", "s2"),
))
