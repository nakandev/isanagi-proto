# from isana.isa import parameter, assembly, binary
# from isana.isa import signed

from .defs import xlen
# from .memory import Mem
# from .register import GPR, GPRC, CSR, PCR
from .instructionType import (
    InstrR, InstrR2, InstrR4, InstrRFloat, InstrR2Float,
    InstrI,
    InstrS,
)


class fld(InstrI):
    opn, opc = "fld", 0b000000000000_00000_011_00000_0000111

    @property
    def is_load(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_pop(self):
        return self.params.inputs['rs1'].number == 2


class fsd(InstrS):
    opn, opc = "fsd", 0b0000000_00000_00000_011_00000_0100111

    @property
    def is_store(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_push(self):
        return self.params.inputs['rs1'].number == 2


class fmadd_d(InstrR4):
    opn, opc = "fmadd.d", 0b00000_01_00000_00000_000_00000_1000011


class fmsub_d(InstrR4):
    opn, opc = "fmsub.d", 0b00000_01_00000_00000_000_00000_1000111


class fnmadd_d(InstrR4):
    opn, opc = "fnmadd.d", 0b00000_01_00000_00000_000_00000_1001011


class fnmsub_d(InstrR4):
    opn, opc = "fnmsub.d", 0b00000_01_00000_00000_000_00000_1001111


class fadd_d(InstrRFloat):
    opn, opc = "fadd.d", 0b0000001_00000_00000_000_00000_1010011


class fsub_d(InstrRFloat):
    opn, opc = "fsub.d", 0b0000101_00000_00000_000_00000_1010011


class fmul_d(InstrRFloat):
    opn, opc = "fmul.d", 0b0001001_00000_00000_000_00000_1010011


class fdiv_d(InstrRFloat):
    opn, opc = "fdiv.d", 0b0001101_00000_00000_000_00000_1010011


class fsqrt_d(InstrR2Float):
    opn, opc = "fsqrt.d", 0b0101101_00000_00000_000_00000_1010011


class fsgnj_d(InstrR):
    opn, opc = "fsgnj.d", 0b0010001_00000_00000_000_00000_1010011


class fsgnjn_d(InstrR):
    opn, opc = "fsgnjn.d", 0b0010001_00000_00000_001_00000_1010011


class fsgnjx_d(InstrR):
    opn, opc = "fsgnjx.d", 0b0010001_00000_00000_010_00000_1010011


class fmin_d(InstrR):
    opn, opc = "fmin.d", 0b0010101_00000_00000_000_00000_1010011


class fmax_d(InstrR):
    opn, opc = "fmin.d", 0b0010101_00000_00000_001_00000_1010011


class fcvt_s_d(InstrR2Float):
    opn, opc = "fcvt.s.d", 0b0100000_00001_00000_000_00000_1010011


class fcvt_d_s(InstrR2Float):
    opn, opc = "fcvt.d.s", 0b0100001_00000_00000_000_00000_1010011


class feq_d(InstrR):
    opn, opc = "feq.d", 0b1010001_00000_00000_010_00000_1010011


class flt_d(InstrR):
    opn, opc = "flt.d", 0b1010001_00000_00000_001_00000_1010011


class fle_d(InstrR):
    opn, opc = "fle.d", 0b1010001_00000_00000_000_00000_1010011


class fclass_d(InstrR):
    opn, opc = "fclass.d", 0b1110001_00000_00000_001_00000_1010011


class fcvt_w_d(InstrR2Float):
    opn, opc = "fcvt.w.d", 0b1100001_00000_00000_000_00000_1010011


class fcvt_wu_d(InstrR2Float):
    opn, opc = "fcvt.wu.d", 0b1100001_00001_00000_000_00000_1010011


class fcvt_d_w(InstrR2Float):
    opn, opc = "fcvt.d.w", 0b1101001_00000_00000_000_00000_1010011


class fcvt_d_wu(InstrR2Float):
    opn, opc = "fcvt.d.wu", 0b1101001_00001_00000_000_00000_1010011


class fcvt_l_d(InstrR2Float):
    opn, opc = "fcvt.l.d", 0b1100001_00010_00000_000_00000_1010011


class fcvt_lu_d(InstrR2Float):
    opn, opc = "fcvt.lu.d", 0b1100001_00011_00000_000_00000_1010011


class fmv_x_d(InstrR2):
    opn, opc = "fmv.x.d", 0b1110001_00000_00000_000_00000_1010011


class fcvt_d_l(InstrR2Float):
    opn, opc = "fcvt.d.l", 0b1101001_00010_00000_000_00000_1010011


class fcvt_d_lu(InstrR2Float):
    opn, opc = "fcvt.d.lu", 0b1101001_00011_00000_000_00000_1010011


class fmv_d_x(InstrR2):
    opn, opc = "fmv.d.x", 0b1111001_00000_00000_000_00000_1010011


# D
instructionsD = [
    fld,
    fsd,
    fmadd_d,
    fmsub_d,
    fnmadd_d,
    fnmsub_d,
    fadd_d,
    fsub_d,
    fmul_d,
    fdiv_d,
    fsqrt_d,
    fsgnj_d,
    fsgnjn_d,
    fsgnjx_d,
    fmin_d,
    fmax_d,
    fcvt_s_d,
    fcvt_d_s,
    feq_d,
    flt_d,
    fle_d,
    fclass_d,
    fcvt_w_d,
    fcvt_wu_d,
    fcvt_d_w,
    fcvt_d_wu,
]

if xlen == 64:
    instructionsD += [
        fcvt_l_d,
        fcvt_lu_d,
        fmv_x_d,
        fcvt_d_l,
        fcvt_d_lu,
        fmv_d_x,
    ]
