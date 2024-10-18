from isana.isa import RegisterGroup, Register

GPR = RegisterGroup("GPR", width=32, regs=(
    Register(0, "x0", "zero"),
    Register(1, "x1", "ra"),
    Register(2, "x2", "sp"),
    Register(3, "x3", "fp"),
    Register(4, "x4", "a0"),
    Register(5, "x5", "a1"),
    Register(6, "x6", "a2"),
    Register(7, "x7", "a3"),
    Register(8, "x8", "s0"),
    Register(9, "x9", "s1"),
    Register(10, "x10", "s2"),
    Register(11, "x11", "s3"),
    Register(12, "x12", "t0"),
    Register(13, "x13", "t1"),
    Register(14, "x14", "t2"),
    Register(15, "x15", "t3"),
))

PCR = RegisterGroup("PCR", width=32, regs=(
    Register(0, "pc", dwarf_number=32),
    Register(1, "prev_pc", dwarf_number=33),
))
