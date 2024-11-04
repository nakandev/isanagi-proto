import itertools
import random
import sys


def byteswap(value, bytesize):
    bs = value.to_bytes(bytesize)
    bs = reversed(bs)
    new_value = int.from_bytes(bs)
    return new_value


class TestBits():
    def __init__(self, msb, lsb, offset):
        self.msb = msb - lsb + offset
        self.lsb = lsb + offset

    def zero(self):
        return 0

    def one(self):
        return 2 ** self.lsb

    def umax(self):
        v = 2 ** (self.msb + 1) - 1
        v -= 2 ** (self.lsb) - 1
        return v

    def smin(self):
        v = 2 ** (self.msb)
        return v

    def smax(self):
        v = 2 ** (self.msb) - 1
        v -= 2 ** (self.lsb) - 1
        return v

    def rand(self):
        v = random.randrange(self.one(), self.umax() + 1)
        return v


class TestOperand():
    def __init__(self, tp, param, isa):
        self.tp = tp
        self.param = param
        self.isa = isa

    def _get_reg_min_max(self, tp):
        group = None
        for group_ in self.isa.registers:
            if tp == group_.label:
                group = group_
                break
        else:
            return (None, None)
        min_ = sys.maxsize
        max_ = 0
        for reg in group.regs:
            min_ = min(min_, reg.idx)
            max_ = max(max_, reg.idx)
        return (min_, max_)

    def _get_imm_min_max(self, tp):
        imm = None
        for imm_ in self.isa.immediates:
            if tp == imm_.label:
                imm = imm_
                break
        else:
            return (None, None)
        if hasattr(imm, "signed"):
            min_ = imm.signed(2 ** (imm.width - 1))
            max_ = imm.signed(2 ** (imm.width - 1) - 1)
        else:
            min_ = 0
            max_ = 2 ** imm.width - 1
        return (min_, max_)

    def zero(self):
        param = self.param
        tp = self.tp
        if self.isa.is_opc_type(tp):
            pass
        elif self.isa.is_reg_type(tp):
            param.number = 0
            param.value = None
        elif self.isa.is_imm_type(tp):
            param.number = None
            param.value = 0
        return self.param

    def one(self):
        param = self.param
        tp = self.tp
        if self.isa.is_opc_type(tp):
            pass
        elif self.isa.is_reg_type(tp):
            param.number = 1
            param.value = None
        elif self.isa.is_imm_type(tp):
            param.number = None
            param.value = 1
        return self.param

    def min(self):
        param = self.param
        tp = self.tp
        if self.isa.is_opc_type(tp):
            pass
        elif self.isa.is_reg_type(tp):
            min_, max_ = self._get_reg_min_max(tp)
            param.number = min_
        elif self.isa.is_imm_type(tp):
            min_, max_ = self._get_imm_min_max(tp)
            param.number = None
            param.value = min_
        return self.param

    def max(self):
        param = self.param
        tp = self.tp
        if self.isa.is_opc_type(tp):
            pass
        elif self.isa.is_reg_type(tp):
            min_, max_ = self._get_reg_min_max(tp)
            param.number = max_
            param.value = None
        elif self.isa.is_imm_type(tp):
            min_, max_ = self._get_imm_min_max(tp)
            param.number = None
            param.value = max_
        return self.param

    def rand(self):
        param = self.param
        tp = self.tp
        if self.isa.is_opc_type(tp):
            pass
        elif self.isa.is_reg_type(tp):
            min_, max_ = self._get_reg_min_max(tp)
            param.number = random.randrange(min_, max_ + 1)
            param.value = None
        elif self.isa.is_imm_type(tp):
            min_, max_ = self._get_imm_min_max(tp)
            param.number = None
            param.value = random.randrange(min_, max_ + 1)
        return self.param


class InstructionTest():
    def __init__(self, isa, instr):
        self.isa = isa
        self.instr = instr()
        self.instr.isa = self.isa

    def gen_binary_edge_case(self):
        len_bits_ex_opc = len([b for b in self.instr.bin.bitss if b.label != "$opc"])
        valuefuncs = [
            TestBits.zero,
            TestBits.one,
            TestBits.smin,
            TestBits.smax,
            TestBits.umax,
        ]
        valuefuncs = list(itertools.product(valuefuncs, repeat=len_bits_ex_opc))
        res = self.gen_binary_case(valuefuncs)
        return res

    def gen_binary_random_case(self, repeat=1):
        len_bits_ex_opc = len([b for b in self.instr.bin.bitss if b.label != "$opc"])
        valuefuncs = [[TestBits.rand] * len_bits_ex_opc] * repeat
        res = self.gen_binary_case(valuefuncs)
        return res

    def gen_binary_case(self, valuefuncs):
        offsets = []
        sum_bits = 0
        for bits in reversed(self.instr.bin.bitss):
            offsets.append(sum_bits)
            sum_bits += bits.msb - bits.lsb + 1
        offsets.reverse()

        res = []
        for vfi in range(len(valuefuncs)):
            value = 0
            funcstrs = []
            bi_ex_opc = 0
            for bi, bits in enumerate(self.instr.bin.bitss):
                msb = bits.msb + offsets[bi]
                lsb = bits.lsb + offsets[bi]
                tbits = TestBits(bits.msb, bits.lsb, offsets[bi])
                if bits.label == "$opc":
                    tvalue = self.instr.opc
                    tvalue &= ((2 ** (msb + 1) - 1) - (2 ** lsb - 1))
                    funcstr = bits.label
                else:
                    funcstr = "{}:{}".format(
                        bits.label,
                        valuefuncs[vfi][bi_ex_opc].__name__,
                    )
                    tvalue = valuefuncs[vfi][bi_ex_opc](tbits)
                value += tvalue
                funcstrs.append(funcstr)
                if bits.label != "$opc":
                    bi_ex_opc += 1
            if self.isa.endian == "big":
                value = byteswap(value, self.instr.bytesize)
            res.append({'value': value, 'func': funcstrs})
        return res

    def gen_asm_edge_case(self):
        len_ops_ex_opc = 0
        for ast in self.instr.asm.ast:
            if ast[0] == "$" and ast != "$opn":
                len_ops_ex_opc += 1
        valuefuncs = [
            TestOperand.zero,
            TestOperand.one,
            TestOperand.min,
            TestOperand.max,
        ]
        valuefuncs = list(itertools.product(valuefuncs, repeat=len_ops_ex_opc))
        res = self.gen_asm_case(valuefuncs)
        return res

    def gen_asm_random_case(self, repeat=1):
        len_ops_ex_opc = 0
        for ast in self.instr.asm.ast:
            if ast[0] == "$" and ast != "$opn":
                len_ops_ex_opc += 1
        valuefuncs = [[TestOperand.rand] * len_ops_ex_opc] * repeat
        res = self.gen_asm_case(valuefuncs)
        return res

    def gen_asm_case(self, valuefuncs):
        res = []
        for vfi in range(len(valuefuncs)):
            self.instr.decode(self.instr.opc)
            asm = ""
            funcstrs = []
            opi_ex_opc = 0
            for ast in self.instr.asm.ast:
                if ast == "$opn":
                    asm += self.instr.opn
                elif ast[0] == "$":
                    label = ast[1:]
                    if label in self.instr.prm.outputs:
                        tp = self.instr.prm.outputs[label]
                        param = self.instr.params.outputs[label]
                        top = TestOperand(tp, param, self.isa)
                        tparam = valuefuncs[vfi][opi_ex_opc](top)
                        asm += self.isa.param_str(tparam)
                    elif label in self.instr.params.inputs:
                        tp = self.instr.prm.inputs[label]
                        param = self.instr.params.inputs[label]
                        top = TestOperand(tp, param, self.isa)
                        tparam = valuefuncs[vfi][opi_ex_opc](top)
                        asm += self.isa.param_str(tparam)
                    else:
                        asm += "#" + ast
                    funcstr = "{}:{}".format(
                        ast,
                        valuefuncs[vfi][opi_ex_opc].__name__,
                    )
                    opi_ex_opc += 1
                    funcstrs.append(funcstr)
                else:
                    asm += ast
            res.append({'asm': asm, 'func': funcstrs})
        return res
