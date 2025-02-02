from isana.isa import Immediate, ImmS

Imm = Immediate("Imm", width=32)
ImmS12 = ImmS("ImmS12", width=12)
ImmS13 = ImmS("ImmS13", width=13)
ImmS21 = ImmS("ImmS21", width=21)
ImmHi20 = Immediate("ImmHi20", width=20, offset=12)
ImmS6 = ImmS("ImmS6", width=6)
ImmS9 = ImmS("ImmS9", width=9)
RMImm = Immediate("RMImm", width=3, enums={
    0: "rne",
    1: "rtz",
    2: "rdn",
    3: "rup",
    4: "rmm",
    7: "dyn",
})
