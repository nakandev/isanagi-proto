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


class flh(InstrI):
    opn, opc = "flh", 0b000000000000_00000_001_00000_0000111

    @property
    def is_load(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_pop(self):
        return self.params.inputs['rs1'].number == 2


class fsh(InstrS):
    opn, opc = "fsh", 0b0000000_00000_00000_001_00000_0100111

    @property
    def is_store(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_push(self):
        return self.params.inputs['rs1'].number == 2


class fmadd_h(InstrR4):
    opn, opc = "fmadd.h", 0b00000_10_00000_00000_000_00000_1000011


class fmsub_h(InstrR4):
    opn, opc = "fmsub.h", 0b00000_10_00000_00000_000_00000_1000111


class fnmadd_h(InstrR4):
    opn, opc = "fnmadd.h", 0b00000_10_00000_00000_000_00000_1001011


class fnmsub_h(InstrR4):
    opn, opc = "fnmsub.h", 0b00000_10_00000_00000_000_00000_1001111


class fadd_h(InstrRFloat):
    opn, opc = "fadd.h", 0b0000010_00000_00000_000_00000_1010011


class fsub_h(InstrRFloat):
    opn, opc = "fsub.h", 0b0000110_00000_00000_000_00000_1010011


class fmul_h(InstrRFloat):
    opn, opc = "fmul.h", 0b0001010_00000_00000_000_00000_1010011


class fdiv_h(InstrRFloat):
    opn, opc = "fdiv.h", 0b0001110_00000_00000_000_00000_1010011


class fsqrt_h(InstrR2Float):
    opn, opc = "fsqrt.h", 0b0101110_00000_00000_000_00000_1010011


class fsgnj_h(InstrR):
    opn, opc = "fsgnj.h", 0b0010010_00000_00000_000_00000_1010011


class fsgnjn_h(InstrR):
    opn, opc = "fsgnjn.h", 0b0010010_00000_00000_001_00000_1010011


class fsgnjx_h(InstrR):
    opn, opc = "fsgnjx.h", 0b0010010_00000_00000_010_00000_1010011


class fmin_h(InstrR):
    opn, opc = "fmin.h", 0b0010110_00000_00000_000_00000_1010011


class fmax_h(InstrR):
    opn, opc = "fmin.h", 0b0010110_00000_00000_001_00000_1010011


class fcvt_s_h(InstrR2Float):
    opn, opc = "fcvt.s.h", 0b0100000_00010_00000_000_00000_1010011


class fcvt_h_s(InstrR2Float):
    opn, opc = "fcvt.h.s", 0b0100010_00000_00000_000_00000_1010011


class fcvt_d_h(InstrR2Float):
    opn, opc = "fcvt.d.h", 0b0100001_00010_00000_000_00000_1010011


class fcvt_h_d(InstrR2Float):
    opn, opc = "fcvt.h.d", 0b0100010_00001_00000_000_00000_1010011


class fcvt_q_h(InstrR2Float):
    opn, opc = "fcvt.q.h", 0b0100011_00010_00000_000_00000_1010011


class fcvt_h_q(InstrR2Float):
    opn, opc = "fcvt.h.q", 0b0100010_00011_00000_000_00000_1010011


class feq_h(InstrR):
    opn, opc = "feq.h", 0b1010000_00000_00000_010_00000_1010011


class flt_h(InstrR):
    opn, opc = "flt.h", 0b1010000_00000_00000_001_00000_1010011


class fle_h(InstrR):
    opn, opc = "fle.h", 0b1010000_00000_00000_000_00000_1010011


class fclass_h(InstrR):
    opn, opc = "fclass.h", 0b1110000_00000_00000_001_00000_1010011


class fcvt_w_h(InstrR2Float):
    opn, opc = "fcvt.w.h", 0b1100000_00000_00000_000_00000_1010011


class fcvt_wu_h(InstrR2Float):
    opn, opc = "fcvt.wu.h", 0b1100000_00001_00000_000_00000_1010011


class fmv_x_h(InstrR2):
    opn, opc = "fmv.x.h", 0b1110000_00000_00000_000_00000_1010011


class fcvt_h_w(InstrR2Float):
    opn, opc = "fcvt.h.w", 0b1101000_00000_00000_000_00000_1010011


class fcvt_h_wu(InstrR2Float):
    opn, opc = "fcvt.h.wu", 0b1101000_00001_00000_000_00000_1010011


class fmv_h_x(InstrR2):
    opn, opc = "fmv.h.x", 0b1111000_00000_00000_000_00000_1010011


class fcvt_l_h(InstrR2Float):
    opn, opc = "fcvt.l.h", 0b1100000_00010_00000_000_00000_1010011


class fcvt_lu_h(InstrR2Float):
    opn, opc = "fcvt.lu.h", 0b1100000_00011_00000_000_00000_1010011


class fcvt_h_l(InstrR2Float):
    opn, opc = "fcvt.h.l", 0b1101000_00010_00000_000_00000_1010011


class fcvt_h_lu(InstrR2Float):
    opn, opc = "fcvt.h.lu", 0b1101000_00011_00000_000_00000_1010011


# Zfh
instructionsZfh = [
    flh,
    fsh,
    fmadd_h,
    fmsub_h,
    fnmadd_h,
    fnmsub_h,
    fadd_h,
    fsub_h,
    fmul_h,
    fdiv_h,
    fsqrt_h,
    fsgnj_h,
    fsgnjn_h,
    fsgnjx_h,
    fmin_h,
    fmax_h,
    fcvt_s_h,
    fcvt_h_s,
    fcvt_d_h,
    fcvt_h_d,
    fcvt_q_h,
    fcvt_h_q,
    feq_h,
    flt_h,
    fle_h,
    fclass_h,
    fcvt_w_h,
    fcvt_wu_h,
    fmv_x_h,
    fcvt_h_w,
    fcvt_h_wu,
    fmv_h_x,
]

if xlen == 64:
    instructionsZfh += [
        fcvt_l_h,
        fcvt_lu_h,
        fcvt_h_l,
        fcvt_h_lu,
    ]
