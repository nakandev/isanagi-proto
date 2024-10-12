from isana.isa import Instruction
from isana.isa import parameter, assembly, binary
# from isana.isa import signed
# from isana.isa import unimpl

# from .memory import Mem
# from .register import GPR, GPRC, VPR, CSR, PC


# Type for Base Instruction Set
class InstrR(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR, rs2:GPR")
    asm = assembly("$opn $rd, $rs1, $rs2")
    bin = binary("$opc[31:25], $rs2[4:0], $rs1[4:0], $opc[14:12], $rd[4:0], $opc[6:0]")


class InstrR2(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR")
    asm = assembly("$opn $rd, $rs1")
    bin = binary("$opc[31:25], $opc[24:20], $rs1[4:0], $opc[14:12], $rd[4:0], $opc[6:0]")


class InstrR4(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR, rs2:GPR, rs3:GPR, rm:Imm")
    asm = assembly("$opn $rd, $rs1, $rs2, $rs3")
    bin = binary("$rs3[4:0], $opc[26:25], $rs2[4:0], $rs1[4:0], $rm[2:0], $rd[4:0], $opc[6:0]")


class InstrRFloat(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR, rs2:GPR, rm:Imm")
    asm = assembly("$opn $rd, $rs1, $rs2")
    bin = binary("$opc[31:25], $rs2[4:0], $rs1[4:0], $rm[2:0], $rd[4:0], $opc[6:0]")


class InstrR2Float(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR, rm:Imm")
    asm = assembly("$opn $rd, $rs1, $rs2")
    bin = binary("$opc[31:25], $opc[24:20], $rs1[4:0], $rm[2:0], $rd[4:0], $opc[6:0]")


class InstrI(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR, imm:ImmS12")
    asm = assembly("$opn $rd, $rs1, $imm")
    bin = binary("$imm[11:0], $rs1[4:0], $opc[14:12], $rd[4:0], $opc[6:0]")


class InstrIShift(InstrI):
    prm = parameter("rd:GPR", "rs1:GPR, imm:Imm")
    asm = assembly("$opn $rd, $rs1, $imm")
    bin = binary("$opc[31:25], $imm[4:0], $rs1[4:0], $opc[14:12], $rd[4:0], $opc[6:0]")


class InstrIShift64(InstrI):
    prm = parameter("rd:GPR", "rs1:GPR, imm:Imm")
    asm = assembly("$opn $rd, $rs1, $imm")
    bin = binary("$opc[31:26], $imm[5:0], $rs1[4:0], $opc[14:12], $rd[4:0], $opc[6:0]")


class InstrILoad(InstrI):
    asm = assembly("$opn $rd, $imm ($rs1)")


class InstrS(Instruction):
    prm = parameter("rs2:GPR", "rs1:GPR, imm:ImmS12")
    asm = assembly("$opn $rs2, $imm ($rs1)")
    bin = binary("$imm[11:5], $rs2[4:0], $rs1[4:0], $opc[14:12], $imm[4:0], $opc[6:0]")


class InstrB(Instruction):
    prm = parameter("rs1:GPR", "rs2:GPR, imm:ImmS13")
    asm = assembly("$opn $rs1, $rs2, $imm")
    bin = binary("$imm[12], $imm[10:5], $rs2[4:0], $rs1[4:0], $opc[14:12], $imm[4:1], $imm[11], $opc[6:0]")


class InstrU(Instruction):
    prm = parameter("rd:GPR", "imm:Imm")
    asm = assembly("$opn $rd, $imm")
    bin = binary("$imm[31:12], $rd[4:0], $opc[6:0]")


class InstrJ(Instruction):
    prm = parameter("rd:GPR", "imm:ImmS21")
    asm = assembly("$opn $rd, $imm")
    bin = binary("$imm[20], $imm[10:1], $imm[11], $imm[19:12], $rd[4:0], $opc[6:0]")


class InstrO(Instruction):
    prm = parameter("", "")
    asm = assembly("$opn")
    bin = binary("$opc[31:0]")


class InstrCSRR(Instruction):
    prm = parameter("rd:GPR, csr:CSR", "csr:CSR, rs1:GPR")
    asm = assembly("$opn $rd, $csr, $rs1")
    bin = binary("$csr[11:0], $rs1[4:0], $opc[14:12], $rd[4:0], $opc[6:0]")


class InstrCSRI(Instruction):
    prm = parameter("rd:GPR, csr:CSR", "csr:CSR, imm:Imm")
    asm = assembly("$opn $rd, $csr, $imm")
    bin = binary("$csr[11:0], $imm[4:0], $opc[14:12], $rd[4:0], $opc[6:0]")


# Type for C-extention
class InstrCR(Instruction):
    prm = parameter("rdrs1:GPR", "rs2:GPR")
    asm = assembly("$opn $rdrs1, $rs2")
    bin = binary("$opc[15:12], $rdrs1[4:0], $rs2[4:0], $opc[1:0]")


class InstrCI(Instruction):
    prm = parameter("rdrs1:GPR", "imm:ImmS6")
    asm = assembly("$opn $rdrs1, $imm")
    bin = binary("$opc[15:13], $imm[5], $rdrs1[4:0], $imm[4:0], $opc[1:0]")


class InstrCSS(Instruction):
    prm = parameter("", "rs2:GPR, imm:ImmS6")
    asm = assembly("$opn $rs2, $imm")
    bin = binary("$opc[15:13], $imm[5:0], $rs2[4:0], $opc[1:0]")


class InstrCIW(Instruction):
    prm = parameter("rd:GPRC", "imm:Imm")
    asm = assembly("$opn $rd, $imm")
    bin = binary("$opc[15:13], $imm[7:0], $rd[2:0], $opc[1:0]")


class InstrCL(Instruction):
    prm = parameter("rd:GPRC", "rs1:GPRC, imm:Imm")
    asm = assembly("$opn $rd, $imm ($rs1)")
    bin = binary("$opc[15:13], $imm[4:2], $rs1[2:0], $imm[1:0], $rd[2:0], $opc[1:0]")


class InstrCS(Instruction):
    prm = parameter("", "rs2:GPRC, rs1:GPRC, imm:Imm")
    asm = assembly("$opn $rs2, $imm ($rs1)")
    bin = binary("$opc[15:13], $imm[4:2], $rs1[2:0], $imm[1:0], $rs2[2:0], $opc[1:0]")


class InstrCA(Instruction):
    prm = parameter("rdrs1:GPRC", "rdrs1:GPRC, rs2:GPRC")
    asm = assembly("$opn $rdrs1, $rs2")
    bin = binary("$opc[15:10], $rdrs1[2:0], $opc[6:5], $rs2[2:0], $opc[1:0]")


class InstrCB(Instruction):
    prm = parameter("rdrs1:GPRC", "rdrs1:GPRC, imm:ImmS9")
    asm = assembly("$opn $rdrs1, $imm")
    bin = binary("$opc[15:13], $imm[7:5], $rdrs1[2:0], $imm[4:0], $opc[1:0]")


class InstrCJ(Instruction):
    prm = parameter("", "imm:ImmS12")
    asm = assembly("$opn $imm")
    bin = binary("$opc[15:13], $imm[11:0], $opc[1:0]")


class InstrCLB(Instruction):
    prm = parameter("rd:GPRC", "rd:GPRC, rs1:GPRC, imm:Imm")
    asm = assembly("$opn $rd, $imm ($rs1)")
    bin = binary("$opc[15:10], $rs1[2:0], $imm[1:0], $rd[2:0], $opc[1:0]")


class InstrCSB(Instruction):
    prm = parameter("", "rs2:GPRC, rs1:GPRC, imm:Imm")
    asm = assembly("$opn $rs2, $imm ($rs1)")
    bin = binary("$opc[15:10], $rs1[2:0], $imm[1:0], $rs2[2:0], $opc[1:0]")


class InstrCLH(Instruction):
    prm = parameter("rd:GPRC", "rd:GPRC, rs1:GPRC, imm:Imm")
    asm = assembly("$opn $rd, $imm ($rs1)")
    bin = binary("$opc[15:10], $rs1[2:0], $opc[6], $imm[0], $rd[2:0], $opc[1:0]")


class InstrCSH(Instruction):
    prm = parameter("", "rs2:GPRC, rs1:GPRC, imm:Imm")
    asm = assembly("$opn $rs2, $imm ($rs1)")
    bin = binary("$opc[15:10], $rs1[2:0], $opc[6], $imm[0], $rs2[2:0], $opc[1:0]")


class InstrCU(Instruction):
    prm = parameter("rdrs1:GPRC", "rdrs1:GPRC")
    asm = assembly("$opn $rdrs1")
    bin = binary("$opc[15:10], $rdrs1[2:0], $opc[6:2], $opc[1:0]")


class InstrCMMV(Instruction):
    prm = parameter("", "rs1:GPRC, rs2:GPRC")
    asm = assembly("$opn $rs1, $rs2")
    bin = binary("$opc[15:10], $rs1[2:0], $opc[6:5], $rs2[2:0], $opc[1:0]")


class InstrCMJT(Instruction):
    prm = parameter("", "imm:Imm")
    asm = assembly("$opn $imm")
    bin = binary("$opc[15:10], $imm[7:0], $opc[1:0]")


class InstrCMPP(Instruction):
    prm = parameter("", "rlist:Imm, imm:Imm")
    asm = assembly("$opn $rlist, $imm")
    bin = binary("$opc[15:10], $opc[9:8], $rlist[3:0], $imm[5:4], $opc[1:0]")


# Type for V-extention
class InstrVLoadFP0(Instruction):
    prm = parameter("vd:VPR", "rs1:GPR, vm:Imm")
    asm = assembly("$opn $rd, $rs1")
    bin = binary("$opc[31:25], $opc[24:20], $rs1[4:0], $opc[14:12], $vd[4:0], $opc[6:0]")


class InstrVLoadFP1(Instruction):
    prm = parameter("vd:VPR", "rs1:GPR, rs2:GPR, vm:Imm")
    asm = assembly("$opn $vd, $rs1, $rs2")
    bin = binary("$opc[31:25], $rs2[4:0], $rs1[4:0], $opc[14:12], $vd[4:0], $opc[6:0]")


class InstrVLoadFP2(Instruction):
    prm = parameter("vd:VPR", "rs1:GPR, vs2:VPR, vm:Imm")
    asm = assembly("$opn $vd, $rs1, $vs2")
    bin = binary("$opc[31:25], $vs2[4:0], $rs1[4:0], $opc[14:12], $vd[4:0], $opc[6:0]")


class InstrVStoreFP0(Instruction):
    prm = parameter("vs3:VPR", "rs1:GPR, vm:Imm")
    asm = assembly("$opn $rs1, $vs3")
    bin = binary("$opc[31:25], $opc[24:20], $rs1[4:0], $opc[14:12], $vs3[4:0], $opc[6:0]")


class InstrVStoreFP1(Instruction):
    prm = parameter("vs3:VPR", "rs1:GPR, rs2:GPR, vm:Imm")
    asm = assembly("$opn $rs1, $rs2, $vs3")
    bin = binary("$opc[31:25], $rs2[4:0], $rs1[4:0], $opc[14:12], $vs3[4:0], $opc[6:0]")


class InstrVStoreFP2(Instruction):
    prm = parameter("vs3:VPR", "rs1:GPR, vs2:VPR, vm:Imm")
    asm = assembly("$opn $rs1, $vs2, $vs3")
    bin = binary("$opc[31:25], $vs2[4:0], $rs1[4:0], $opc[14:12], $vs3[4:0], $opc[6:0]")


class InstrVArith0(Instruction):
    prm = parameter("vd:VPR", "vs1:VPR, vs2:VPR, vm:Imm")
    asm = assembly("$opn $vd, $vs1, $vs2")
    bin = binary("$opc[31:25], $vs2[4:0], $rs1[4:0], $opc[14:12], $vd[4:0], $opc[6:0]")


class InstrVArith12(Instruction):
    prm = parameter("vdrd:VGPR", "vs1:VPR, vs2:VPR, vm:Imm")
    asm = assembly("$opn $vdrd, $vs1, $vs2")
    bin = binary("$opc[31:25], $vs2[4:0], $vs1[4:0], $opc[14:12], $vdrd[4:0], $opc[6:0]")


class InstrVArith3(Instruction):
    prm = parameter("vd:VPR", "imm:Imm, vs2:VPR, vm:Imm")
    asm = assembly("$opn $vd, $imm, $vs2")
    bin = binary("$opc[31:25], $vs2[4:0], $imm[4:0], $opc[14:12], $vd[4:0], $opc[6:0]")


class InstrVArith45(Instruction):
    prm = parameter("vd:VPR", "rs1:VPR, vs2:VPR, vm:Imm")
    asm = assembly("$opn $vd, $rs1, $vs2")
    bin = binary("$opc[31:25], $vs2[4:0], $rs1[4:0], $opc[14:12], $vd[4:0], $opc[6:0]")


class InstrVArith6(Instruction):
    prm = parameter("vdrd:VGPR", "rs1:VPR, vs2:VPR, vm:Imm")
    asm = assembly("$opn $vdrd, $rs1, $vs2")
    bin = binary("$opc[31:25], $vs2[4:0], $rs1[4:0], $opc[14:12], $vdrd[4:0], $opc[6:0]")


class InstrVConf0(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR, vtypei:Imm")
    asm = assembly("$opn $rd, $rs1, $vtypei")
    bin = binary("$opc[31], $vtypei[10:0], $rs1[4:0], $opc[14:12], $rd[4:0], $opc[6:0]")


class InstrVConf1(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR, imm:Imm, vtypei:Imm")
    asm = assembly("$opn $rd, $rs1, $imm, $vtypei")
    bin = binary("$opc[31:25], $vtypei[9:0], $imm[4:0], $opc[14:12], $rd[4:0], $opc[6:0]")


class InstrVConf2(Instruction):
    prm = parameter("rd:GPR", "rs1:GPR, rs2:GPR")
    asm = assembly("$opn $rd, $rs1, $rs2")
    bin = binary("$opc[31:25], $rs2[4:0], $rs1[4:0], $opc[14:12], $rd[4:0], $opc[6:0]")
