from isana.isa import RegisterGroup, Register

from .defs import xlen


PCR = RegisterGroup("PCR", width=xlen, regs=(
    Register(0, "pc"),
    Register(1, "prev_pc"),
))


class GPRReg(Register):
    pass


GPR_regs = (
    GPRReg(0, "x0", "zero"),
    GPRReg(1, "x1", "ra", caller=True),
    GPRReg(2, "x2", "sp", callee=True, stackpointer=True),
    GPRReg(3, "x3", "gp", globalpointer=True),
    GPRReg(4, "x4", "tp"),
    GPRReg(5, "x5", "t0", caller=True),
    GPRReg(6, "x6", "t1", caller=True),
    GPRReg(7, "x7", "t2", caller=True),
    GPRReg(8, "x8", "s0", "fp", callee=True),
    GPRReg(9, "x9", "s1", callee=True),
    GPRReg(10, "x10", "a0", caller=True),
    GPRReg(11, "x11", "a1", caller=True),
    GPRReg(12, "x12", "a2", caller=True),
    GPRReg(13, "x13", "a3", caller=True),
    GPRReg(14, "x14", "a4", caller=True),
    GPRReg(15, "x15", "a5", caller=True),
    GPRReg(16, "x16", "a6", caller=True),
    GPRReg(17, "x17", "a7", caller=True),
    GPRReg(18, "x18", "s2", callee=True),
    GPRReg(19, "x19", "s3", callee=True),
    GPRReg(20, "x20", "s4", callee=True),
    GPRReg(21, "x21", "s5", callee=True),
    GPRReg(22, "x22", "s6", callee=True),
    GPRReg(23, "x23", "s7", callee=True),
    GPRReg(24, "x24", "s8", callee=True),
    GPRReg(25, "x25", "s9", callee=True),
    GPRReg(26, "x26", "s10", callee=True),
    GPRReg(27, "x27", "s11", callee=True),
    GPRReg(28, "x28", "t3", caller=True),
    GPRReg(29, "x29", "t4", caller=True),
    GPRReg(30, "x30", "t5", caller=True),
    GPRReg(31, "x31", "t6", caller=True),
)

GPR = RegisterGroup("GPR", width=xlen, regs=(
    GPR_regs[:]
))

GPRC = RegisterGroup("GPRC", width=xlen, regs=(
    GPR_regs[8:16]
))


class FPRReg(Register):
    pass


FPR = RegisterGroup("FPR", width=xlen, regs=(
    FPRReg(0, "f0", "ft0", caller=True),
    FPRReg(1, "f1", "ft1", caller=True),
    FPRReg(2, "f2", "ft2", caller=True),
    FPRReg(3, "f3", "ft3", caller=True),
    FPRReg(4, "f4", "ft4", caller=True),
    FPRReg(5, "f5", "ft5", caller=True),
    FPRReg(6, "f6", "ft6", caller=True),
    FPRReg(7, "f7", "ft7", caller=True),
    FPRReg(8, "f8", "fs1", callee=True),
    FPRReg(9, "f9", "fs2", callee=True),
    FPRReg(10, "f10", "fa0", caller=True),
    FPRReg(11, "f11", "fa1", caller=True),
    FPRReg(12, "f12", "fa2", caller=True),
    FPRReg(13, "f13", "fa3", caller=True),
    FPRReg(14, "f14", "fa4", caller=True),
    FPRReg(15, "f15", "fa5", caller=True),
    FPRReg(16, "f16", "fa6", caller=True),
    FPRReg(17, "f17", "fa7", caller=True),
    FPRReg(18, "f18", "fs2", callee=True),
    FPRReg(19, "f19", "fs3", callee=True),
    FPRReg(20, "f20", "fs4", callee=True),
    FPRReg(21, "f21", "fs5", callee=True),
    FPRReg(22, "f22", "fs6", callee=True),
    FPRReg(23, "f23", "fs7", callee=True),
    FPRReg(24, "f24", "fs8", callee=True),
    FPRReg(25, "f25", "fs9", callee=True),
    FPRReg(26, "f26", "fs10", callee=True),
    FPRReg(27, "f27", "fs11", callee=True),
    FPRReg(28, "f28", "ft8", caller=True),
    FPRReg(29, "f29", "ft9", caller=True),
    FPRReg(30, "f30", "ft10", caller=True),
    FPRReg(31, "f31", "ft11", caller=True),
))

VPR = RegisterGroup("VPR", width=xlen, regs=(
))

VGPR = RegisterGroup("VGPR", width=xlen, regs=(
))


class CSRReg(Register):
    pass


CSR = RegisterGroup("CSR", width=xlen, regs=(
    CSRReg(0x001, "fflags"),
    CSRReg(0x002, "frm"),
    CSRReg(0x003, "fcsr"),
    CSRReg(0x011, "ssp"),

    CSRReg(0xC00, "cycle"),
    CSRReg(0xC01, "time"),
    CSRReg(0xC02, "instret"),
    CSRReg(0xC03, "hpmcounter3"),
    CSRReg(0xC04, "hpmcounter4"),
    CSRReg(0xC05, "hpmcounter5"),
    CSRReg(0xC06, "hpmcounter6"),
    CSRReg(0xC07, "hpmcounter7"),
    CSRReg(0xC08, "hpmcounter8"),
    CSRReg(0xC09, "hpmcounter9"),
    CSRReg(0xC0A, "hpmcounter10"),
    CSRReg(0xC0B, "hpmcounter11"),
    CSRReg(0xC0C, "hpmcounter12"),
    CSRReg(0xC0D, "hpmcounter13"),
    CSRReg(0xC0E, "hpmcounter14"),
    CSRReg(0xC0F, "hpmcounter15"),
    CSRReg(0xC10, "hpmcounter16"),
    CSRReg(0xC11, "hpmcounter17"),
    CSRReg(0xC12, "hpmcounter18"),
    CSRReg(0xC13, "hpmcounter19"),
    CSRReg(0xC14, "hpmcounter20"),
    CSRReg(0xC15, "hpmcounter21"),
    CSRReg(0xC16, "hpmcounter22"),
    CSRReg(0xC17, "hpmcounter23"),
    CSRReg(0xC18, "hpmcounter24"),
    CSRReg(0xC19, "hpmcounter25"),
    CSRReg(0xC1A, "hpmcounter26"),
    CSRReg(0xC1B, "hpmcounter27"),
    CSRReg(0xC1C, "hpmcounter28"),
    CSRReg(0xC1D, "hpmcounter29"),
    CSRReg(0xC1E, "hpmcounter30"),
    CSRReg(0xC1F, "hpmcounter31"),
    CSRReg(0xC80, "cycleh"),
    CSRReg(0xC81, "timeh"),
    CSRReg(0xC82, "instreth"),
    CSRReg(0xC83, "hpmcounter3h"),
    CSRReg(0xC84, "hpmcounter4h"),
    CSRReg(0xC85, "hpmcounter5h"),
    CSRReg(0xC86, "hpmcounter6h"),
    CSRReg(0xC87, "hpmcounter7h"),
    CSRReg(0xC88, "hpmcounter8h"),
    CSRReg(0xC89, "hpmcounter9h"),
    CSRReg(0xC8A, "hpmcounter10h"),
    CSRReg(0xC8B, "hpmcounter11h"),
    CSRReg(0xC8C, "hpmcounter12h"),
    CSRReg(0xC8D, "hpmcounter13h"),
    CSRReg(0xC8E, "hpmcounter14h"),
    CSRReg(0xC8F, "hpmcounter15h"),
    CSRReg(0xC90, "hpmcounter16h"),
    CSRReg(0xC91, "hpmcounter17h"),
    CSRReg(0xC92, "hpmcounter18h"),
    CSRReg(0xC93, "hpmcounter19h"),
    CSRReg(0xC94, "hpmcounter20h"),
    CSRReg(0xC95, "hpmcounter21h"),
    CSRReg(0xC96, "hpmcounter22h"),
    CSRReg(0xC97, "hpmcounter23h"),
    CSRReg(0xC98, "hpmcounter24h"),
    CSRReg(0xC99, "hpmcounter25h"),
    CSRReg(0xC9A, "hpmcounter26h"),
    CSRReg(0xC9B, "hpmcounter27h"),
    CSRReg(0xC9C, "hpmcounter28h"),
    CSRReg(0xC9D, "hpmcounter29h"),
    CSRReg(0xC9E, "hpmcounter30h"),
    CSRReg(0xC9F, "hpmcounter31h"),

    CSRReg(0x100, "sstatus"),
    CSRReg(0x104, "sie"),
    CSRReg(0x105, "stvec"),
    CSRReg(0x106, "scounteren"),
    CSRReg(0x10A, "senvcfg"),
    CSRReg(0x120, "scountinhibit"),
    CSRReg(0x140, "sscratch"),
    CSRReg(0x141, "sepc"),
    CSRReg(0x142, "scause"),
    CSRReg(0x143, "stval"),
    CSRReg(0x144, "sip"),
    CSRReg(0xDA0, "scountovf"),
    CSRReg(0x180, "satp"),
    CSRReg(0x5A8, "scontext"),
    CSRReg(0x10C, "sstateen0"),
    CSRReg(0x10D, "sstateen1"),
    CSRReg(0x10E, "sstateen2"),
    CSRReg(0x10F, "sstateen3"),

    CSRReg(0x600, "hstatus"),
    CSRReg(0x602, "hedeleg"),
    CSRReg(0x603, "hideleg"),
    CSRReg(0x604, "hie"),
    CSRReg(0x606, "hcounteren"),
    CSRReg(0x607, "hgeie"),
    CSRReg(0x612, "hedelegh"),
    CSRReg(0x643, "htval"),
    CSRReg(0x644, "hip"),
    CSRReg(0x645, "hvip"),
    CSRReg(0x64A, "htinst"),
    CSRReg(0xE12, "hgeip"),
    CSRReg(0x60A, "henvcfg"),
    CSRReg(0x61A, "henvcfgh"),
    CSRReg(0x680, "hgatp"),
    CSRReg(0x6A8, "hcontext"),
    CSRReg(0x605, "htimedelta"),
    CSRReg(0x615, "htimedeltah"),
    CSRReg(0x60C, "hstateen0"),
    CSRReg(0x60D, "hstateen1"),
    CSRReg(0x60E, "hstateen2"),
    CSRReg(0x60F, "hstateen3"),
    CSRReg(0x61C, "hstateen0h"),
    CSRReg(0x61D, "hstateen1h"),
    CSRReg(0x61E, "hstateen2h"),
    CSRReg(0x61F, "hstateen3h"),
    CSRReg(0x200, "vsstatus"),
    CSRReg(0x204, "vsie"),
    CSRReg(0x205, "vstvec"),
    CSRReg(0x240, "vsscratch"),
    CSRReg(0x241, "vsepc"),
    CSRReg(0x242, "vscause"),
    CSRReg(0x243, "vstval"),
    CSRReg(0x244, "vsip"),
    CSRReg(0x280, "vsatp"),

    CSRReg(0xF11, "mvendorid"),
    CSRReg(0xF12, "marchid"),
    CSRReg(0xF13, "mimpid"),
    CSRReg(0xF14, "mhartid"),
    CSRReg(0xF15, "mconfigptr"),
    CSRReg(0x300, "mstatus"),
    CSRReg(0x301, "misa"),
    CSRReg(0x302, "medeleg"),
    CSRReg(0x303, "mideleg"),
    CSRReg(0x304, "mie"),
    CSRReg(0x305, "mtvec"),
    CSRReg(0x306, "mcounteren"),
    CSRReg(0x310, "mstatush"),
    CSRReg(0x312, "medelegh"),
    CSRReg(0x340, "mscratch"),
    CSRReg(0x341, "mepc"),
    CSRReg(0x342, "mcause"),
    CSRReg(0x343, "mtval"),
    CSRReg(0x344, "mip"),
    CSRReg(0x34A, "mtinst"),
    CSRReg(0x34B, "mtval2"),
    CSRReg(0x30A, "menvcfg"),
    CSRReg(0x31A, "menvcfgh"),
    CSRReg(0x747, "mseccfg"),
    CSRReg(0x757, "mseccfgh"),
    CSRReg(0x3A0, "pmpcfg0"),
    CSRReg(0x3A1, "pmpcfg1"),
    CSRReg(0x3A2, "pmpcfg2"),
    CSRReg(0x3A3, "pmpcfg3"),
    CSRReg(0x3A4, "pmpcfg4"),
    CSRReg(0x3A5, "pmpcfg5"),
    CSRReg(0x3A6, "pmpcfg6"),
    CSRReg(0x3A7, "pmpcfg7"),
    CSRReg(0x3A8, "pmpcfg8"),
    CSRReg(0x3A9, "pmpcfg9"),
    CSRReg(0x3AA, "pmpcfg10"),
    CSRReg(0x3AB, "pmpcfg11"),
    CSRReg(0x3AC, "pmpcfg12"),
    CSRReg(0x3AD, "pmpcfg13"),
    CSRReg(0x3AE, "pmpcfg14"),
    CSRReg(0x3AF, "pmpcfg15"),
    CSRReg(0x3B0, "pmpaddr0"),
    CSRReg(0x3B1, "pmpaddr1"),
    CSRReg(0x3B2, "pmpaddr2"),
    CSRReg(0x3B3, "pmpaddr3"),
    CSRReg(0x3B4, "pmpaddr4"),
    CSRReg(0x3B5, "pmpaddr5"),
    CSRReg(0x3B6, "pmpaddr6"),
    CSRReg(0x3B7, "pmpaddr7"),
    CSRReg(0x3B8, "pmpaddr8"),
    CSRReg(0x3B9, "pmpaddr9"),
    CSRReg(0x3BA, "pmpaddr10"),
    CSRReg(0x3BB, "pmpaddr11"),
    CSRReg(0x3BC, "pmpaddr12"),
    CSRReg(0x3BD, "pmpaddr13"),
    CSRReg(0x3BE, "pmpaddr14"),
    CSRReg(0x3BF, "pmpaddr15"),
    CSRReg(0x3C0, "pmpaddr16"),
    CSRReg(0x3C1, "pmpaddr17"),
    CSRReg(0x3C2, "pmpaddr18"),
    CSRReg(0x3C3, "pmpaddr19"),
    CSRReg(0x3C4, "pmpaddr20"),
    CSRReg(0x3C5, "pmpaddr21"),
    CSRReg(0x3C6, "pmpaddr22"),
    CSRReg(0x3C7, "pmpaddr23"),
    CSRReg(0x3C8, "pmpaddr24"),
    CSRReg(0x3C9, "pmpaddr25"),
    CSRReg(0x3CA, "pmpaddr26"),
    CSRReg(0x3CB, "pmpaddr27"),
    CSRReg(0x3CC, "pmpaddr28"),
    CSRReg(0x3CD, "pmpaddr29"),
    CSRReg(0x3CE, "pmpaddr30"),
    CSRReg(0x3CF, "pmpaddr31"),
    CSRReg(0x3D0, "pmpaddr32"),
    CSRReg(0x3D1, "pmpaddr33"),
    CSRReg(0x3D2, "pmpaddr34"),
    CSRReg(0x3D3, "pmpaddr35"),
    CSRReg(0x3D4, "pmpaddr36"),
    CSRReg(0x3D5, "pmpaddr37"),
    CSRReg(0x3D6, "pmpaddr38"),
    CSRReg(0x3D7, "pmpaddr39"),
    CSRReg(0x3D8, "pmpaddr40"),
    CSRReg(0x3D9, "pmpaddr41"),
    CSRReg(0x3DA, "pmpaddr42"),
    CSRReg(0x3DB, "pmpaddr43"),
    CSRReg(0x3DC, "pmpaddr44"),
    CSRReg(0x3DD, "pmpaddr45"),
    CSRReg(0x3DE, "pmpaddr46"),
    CSRReg(0x3DF, "pmpaddr47"),
    CSRReg(0x3E0, "pmpaddr48"),
    CSRReg(0x3E1, "pmpaddr49"),
    CSRReg(0x3E2, "pmpaddr50"),
    CSRReg(0x3E3, "pmpaddr51"),
    CSRReg(0x3E4, "pmpaddr52"),
    CSRReg(0x3E5, "pmpaddr53"),
    CSRReg(0x3E6, "pmpaddr54"),
    CSRReg(0x3E7, "pmpaddr55"),
    CSRReg(0x3E8, "pmpaddr56"),
    CSRReg(0x3E9, "pmpaddr57"),
    CSRReg(0x3EA, "pmpaddr58"),
    CSRReg(0x3EB, "pmpaddr59"),
    CSRReg(0x3EC, "pmpaddr60"),
    CSRReg(0x3ED, "pmpaddr61"),
    CSRReg(0x3EE, "pmpaddr62"),
    CSRReg(0x3EF, "pmpaddr63"),
    CSRReg(0x30C, "mstateen0"),
    CSRReg(0x30D, "mstateen1"),
    CSRReg(0x30E, "mstateen2"),
    CSRReg(0x30F, "mstateen3"),
    CSRReg(0x31C, "mstateen0h"),
    CSRReg(0x31D, "mstateen1h"),
    CSRReg(0x31E, "mstateen2h"),
    CSRReg(0x31F, "mstateen3h"),
    CSRReg(0x740, "mnscratch"),
    CSRReg(0x741, "mnepc"),
    CSRReg(0x742, "mncause"),
    CSRReg(0x744, "mnstatus"),
    CSRReg(0xB00, "mcycle"),
    CSRReg(0xB02, "minstret"),
    CSRReg(0xB03, "mhpmcounter3"),
    CSRReg(0xB04, "mhpmcounter4"),
    CSRReg(0xB05, "mhpmcounter5"),
    CSRReg(0xB06, "mhpmcounter6"),
    CSRReg(0xB07, "mhpmcounter7"),
    CSRReg(0xB08, "mhpmcounter8"),
    CSRReg(0xB09, "mhpmcounter9"),
    CSRReg(0xB0A, "mhpmcounter10"),
    CSRReg(0xB0B, "mhpmcounter11"),
    CSRReg(0xB0C, "mhpmcounter12"),
    CSRReg(0xB0D, "mhpmcounter13"),
    CSRReg(0xB0E, "mhpmcounter14"),
    CSRReg(0xB0F, "mhpmcounter15"),
    CSRReg(0xB10, "mhpmcounter16"),
    CSRReg(0xB11, "mhpmcounter17"),
    CSRReg(0xB12, "mhpmcounter18"),
    CSRReg(0xB13, "mhpmcounter19"),
    CSRReg(0xB14, "mhpmcounter20"),
    CSRReg(0xB15, "mhpmcounter21"),
    CSRReg(0xB16, "mhpmcounter22"),
    CSRReg(0xB17, "mhpmcounter23"),
    CSRReg(0xB18, "mhpmcounter24"),
    CSRReg(0xB19, "mhpmcounter25"),
    CSRReg(0xB1A, "mhpmcounter26"),
    CSRReg(0xB1B, "mhpmcounter27"),
    CSRReg(0xB1C, "mhpmcounter28"),
    CSRReg(0xB1D, "mhpmcounter29"),
    CSRReg(0xB1E, "mhpmcounter30"),
    CSRReg(0xB1F, "mhpmcounter31"),
    CSRReg(0xB80, "mcycleh"),
    CSRReg(0xB82, "minstreth"),
    CSRReg(0xB83, "mhpmcounter3h"),
    CSRReg(0xB84, "mhpmcounter4h"),
    CSRReg(0xB85, "mhpmcounter5h"),
    CSRReg(0xB86, "mhpmcounter6h"),
    CSRReg(0xB87, "mhpmcounter7h"),
    CSRReg(0xB88, "mhpmcounter8h"),
    CSRReg(0xB89, "mhpmcounter9h"),
    CSRReg(0xB8A, "mhpmcounter10h"),
    CSRReg(0xB8B, "mhpmcounter11h"),
    CSRReg(0xB8C, "mhpmcounter12h"),
    CSRReg(0xB8D, "mhpmcounter13h"),
    CSRReg(0xB8E, "mhpmcounter14h"),
    CSRReg(0xB8F, "mhpmcounter15h"),
    CSRReg(0xB90, "mhpmcounter16h"),
    CSRReg(0xB91, "mhpmcounter17h"),
    CSRReg(0xB92, "mhpmcounter18h"),
    CSRReg(0xB93, "mhpmcounter19h"),
    CSRReg(0xB94, "mhpmcounter20h"),
    CSRReg(0xB95, "mhpmcounter21h"),
    CSRReg(0xB96, "mhpmcounter22h"),
    CSRReg(0xB97, "mhpmcounter23h"),
    CSRReg(0xB98, "mhpmcounter24h"),
    CSRReg(0xB99, "mhpmcounter25h"),
    CSRReg(0xB9A, "mhpmcounter26h"),
    CSRReg(0xB9B, "mhpmcounter27h"),
    CSRReg(0xB9C, "mhpmcounter28h"),
    CSRReg(0xB9D, "mhpmcounter29h"),
    CSRReg(0xB9E, "mhpmcounter30h"),
    CSRReg(0xB9F, "mhpmcounter31h"),
    CSRReg(0x320, "mcountinhibit"),
    CSRReg(0x323, "mhpmevent3"),
    CSRReg(0x324, "mhpmevent4"),
    CSRReg(0x325, "mhpmevent5"),
    CSRReg(0x326, "mhpmevent6"),
    CSRReg(0x327, "mhpmevent7"),
    CSRReg(0x328, "mhpmevent8"),
    CSRReg(0x329, "mhpmevent9"),
    CSRReg(0x32A, "mhpmevent10"),
    CSRReg(0x32B, "mhpmevent11"),
    CSRReg(0x32C, "mhpmevent12"),
    CSRReg(0x32D, "mhpmevent13"),
    CSRReg(0x32E, "mhpmevent14"),
    CSRReg(0x32F, "mhpmevent15"),
    CSRReg(0x330, "mhpmevent16"),
    CSRReg(0x331, "mhpmevent17"),
    CSRReg(0x332, "mhpmevent18"),
    CSRReg(0x333, "mhpmevent19"),
    CSRReg(0x334, "mhpmevent20"),
    CSRReg(0x335, "mhpmevent21"),
    CSRReg(0x336, "mhpmevent22"),
    CSRReg(0x337, "mhpmevent23"),
    CSRReg(0x338, "mhpmevent24"),
    CSRReg(0x339, "mhpmevent25"),
    CSRReg(0x33A, "mhpmevent26"),
    CSRReg(0x33B, "mhpmevent27"),
    CSRReg(0x33C, "mhpmevent28"),
    CSRReg(0x33D, "mhpmevent29"),
    CSRReg(0x33E, "mhpmevent30"),
    CSRReg(0x33F, "mhpmevent31"),
    CSRReg(0x723, "mhpmevent3h"),
    CSRReg(0x724, "mhpmevent4h"),
    CSRReg(0x725, "mhpmevent5h"),
    CSRReg(0x726, "mhpmevent6h"),
    CSRReg(0x727, "mhpmevent7h"),
    CSRReg(0x728, "mhpmevent8h"),
    CSRReg(0x729, "mhpmevent9h"),
    CSRReg(0x72A, "mhpmevent10h"),
    CSRReg(0x72B, "mhpmevent11h"),
    CSRReg(0x72C, "mhpmevent12h"),
    CSRReg(0x72D, "mhpmevent13h"),
    CSRReg(0x72E, "mhpmevent14h"),
    CSRReg(0x72F, "mhpmevent15h"),
    CSRReg(0x730, "mhpmevent16h"),
    CSRReg(0x731, "mhpmevent17h"),
    CSRReg(0x732, "mhpmevent18h"),
    CSRReg(0x733, "mhpmevent19h"),
    CSRReg(0x734, "mhpmevent20h"),
    CSRReg(0x735, "mhpmevent21h"),
    CSRReg(0x736, "mhpmevent22h"),
    CSRReg(0x737, "mhpmevent23h"),
    CSRReg(0x738, "mhpmevent24h"),
    CSRReg(0x739, "mhpmevent25h"),
    CSRReg(0x73A, "mhpmevent26h"),
    CSRReg(0x73B, "mhpmevent27h"),
    CSRReg(0x73C, "mhpmevent28h"),
    CSRReg(0x73D, "mhpmevent29h"),
    CSRReg(0x73E, "mhpmevent30h"),
    CSRReg(0x73F, "mhpmevent31h"),
    CSRReg(0x7A0, "tselect"),
    CSRReg(0x7A1, "tdata1"),
    CSRReg(0x7A2, "tdata2"),
    CSRReg(0x7A3, "tdata3"),
    CSRReg(0x7A8, "mcontext"),
    CSRReg(0x7B0, "dcsr"),
    CSRReg(0x7B1, "dpc"),
    CSRReg(0x7B2, "dscratch0"),
    CSRReg(0x7B3, "dscratch1"),
))
