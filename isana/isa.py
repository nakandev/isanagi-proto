import copy
import re


class Bits():
    def __init__(self, *args, **kwargs):
        bit_slice = r"\s*(\d+)\s*:\s*(\d+)\s*"
        bit_index = r"\s*(\d+)\s*"
        if len(args) == 1 and isinstance(args[0], str):
            try:
                if m := re.match(r"^(\$\w+)\[([^\]]+)\]$", args[0]):
                    self.label = m.group(1)
                    bit_indices = m.group(2)
                    # TODO: verify bit range
                    if m2 := re.match(fr"^{bit_slice}$", bit_indices):
                        self.msb = int(m2.group(1))
                        self.lsb = int(m2.group(2))
                    elif m2 := re.match(fr"^{bit_index}$", bit_indices):
                        self.msb = int(m2.group(1))
                        self.lsb = int(m2.group(1))
                    else:
                        raise ValueError()
                    self.value = 0
                elif m := re.match(r"^(0x|0d)?([0-9a-f]+)\[([^\]]+)\]$", args[0]):
                    self.label = "#"
                    if m.group(1) == "0x":
                        base = 16
                    elif m.group(1) == "0d":
                        base = 10
                    else:
                        base = 2
                    self.value = int(m.group(2), base)
                    bit_indices = m.group(3)
                    # TODO: verify bit range
                    if m2 := re.match(fr"^{bit_slice}$", bit_indices):
                        self.msb = int(m2.group(1))
                        self.lsb = int(m2.group(2))
                    elif m2 := re.match(fr"^{bit_index}$", bit_indices):
                        self.msb = int(m2.group(1))
                        self.lsb = int(m2.group(1))
                    else:
                        raise ValueError()
                else:
                    raise ValueError()
            except ValueError:
                raise ValueError("binary() arguments syntax error: \"{}\"".format(args[0]))
        elif len(args) == 3 or len(args) == 4:
            self.label = args[0]
            self.msb = args[1]
            self.lsb = args[2]
            self.value = args[3] if len(args) == 4 else 0
        elif len(kwargs) > 0:
            self.label = kwargs.get('label', str())
            self.msb = kwargs.get('msb', -1)
            self.lsb = kwargs.get('lsb', -1)
            self.value = kwargs.get('value', 0)
        else:
            self.label = str()
            self.msb = -1
            self.lsb = -1
            self.value = 0

    def __repr__(self):
        return "{}:[{}:{}]={}".format(
            self.label,
            self.msb,
            self.lsb,
            self.value,
        )

    def size(self):
        return self.msb - self.lsb + 1

    def mask(self):
        return 2 ** self.size() - 1

    def pop_value(self, value):
        v = (value & self.mask()) << self.lsb
        nv = value >> self.size()
        return (v, nv)


class ISA():
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.registers = kwargs.pop('registers')
        self.memories = kwargs.pop('memories')
        self.immediates = kwargs.pop('immediates')
        self.instructions = kwargs.pop('instructions')
        self.context = kwargs.pop('context')
        self._ctx = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def is_opc_type(self, tp: str):
        return tp == "Opc"

    def is_reg_type(self, tp: str):
        for reg in self.registers:
            if tp == reg.label:
                return True
        return False

    def is_imm_type(self, tp: str):
        for imm in self.immediates:
            if tp == imm.label:
                return True
        return False

    def get_reg(self, tp: str, idx: int):
        group = None
        for group_ in self.registers:
            if tp == group_.label:
                group = group_
                break
        if group:
            for reg in group.regs:
                if idx == reg.idx:
                    return reg
        return None

    def get_reg_name(self, tp: str, idx: int, alias=True):
        reg = self.get_reg(tp, idx)
        if reg:
            if alias and len(reg.aliases) > 0:
                return reg.aliases[0]
            else:
                return reg.label
        return "<{}:{}>".format(idx, tp)

    def get_imm_str(self, tp: str, value: int, instr: 'Instruction'):
        try:
            s = "{} <{}>".format(str(hex(value)), hex(instr.target_addr()))
        except NotImplementedError:
            s = str(hex(value))
        return s

    def param_str(self, param):
        if self.is_opc_type(param.type_):
            s = param.label
        elif self.is_reg_type(param.type_):
            s = self.get_reg_name(param.type_, param.number)
        elif self.is_imm_type(param.type_):
            s = self.get_imm_str(param.type_, param.value, param.instr)
        else:
            s = "{}:{}".format(param.label, param.type_)
        return s

    def decode(self, value: int, addr: int | None = None):
        return self._decode0(value, addr=addr)

    def _decode0(self, value: int, addr: int | None = None):
        # simple opecode match
        instr = None
        for instr0 in self.instructions:
            instr0 = instr0()
            if instr0.match_opecode(value):
                instr = instr0
                break
        else:
            instr = unknown_op()
        instr.isa = self
        instr.decode(value, addr=addr)
        return instr

    def new_context(self):
        ctx = self.context(
            registers=copy.deepcopy(self.registers),
            memories=copy.deepcopy(self.memories),
            # immediates=copy.deepcopy(self.immediates),
        )
        self._ctx = ctx

    def execute(self, addr=None):
        if addr is None:
            addr = self._ctx.PC.pc
        value = self._ctx.Mem.read(32, addr)
        ins = self.decode(value, addr=addr)
        self._ctx.pre_semantic()
        ins.semantic(self._ctx, ins)
        self._ctx.post_semantic(ins)


class Context():
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.registers = kwargs.get('registers')
        self.memories = kwargs.get('memories')
        # self.immediates = kwargs.pop('immediates')

    def __getattr__(self, key):
        if isinstance(key, str):
            for x in self.registers:
                if key == x.label:
                    return x
            for x in self.memories:
                if key == x.label:
                    return x
        return super().__getattr__(key)

    def pre_semantic(self):
        pass

    def post_semantic(self):
        pass


class RegisterGroup():
    def __init__(self, label: str, **kwargs):
        self.label = label
        self.width = kwargs.get('width')
        self.regs = kwargs.get('regs')
        for reg in self.regs:
            reg.group = self

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < len(self.regs):
                return self.regs[key].value
        raise ValueError()

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key < len(self.regs):
                self.regs[key].value = value
                return
        raise ValueError()

    def __getattr__(self, key):
        if isinstance(key, str) and 'regs' in self.__dict__:
            for reg in self.regs:
                if key == reg.label:
                    return reg.value
        return super().__getattr__(key)

    def __setattr__(self, key, value):
        if isinstance(key, str) and 'regs' in self.__dict__:
            for reg in self.regs:
                if key == reg.label:
                    reg.value = value
                    return
        super().__setattr__(key, value)

    def __iter__(self):
        yield from self.regs


class Register():
    def __init__(self, number: int, label: str, *args, **kwargs):
        self.group = None
        self.number = number
        self.label = label
        self.aliases = args
        self.is_callee_saved = kwargs.get('callee', False)
        self.is_caller_saved = kwargs.get('caller', False)
        self.is_stack_pointer = kwargs.get('stackpointer', False)
        self.is_global_pointer = kwargs.get('globalpointer', False)
        self.idx = kwargs.get('idx', number)
        self.dwarf_number = kwargs.get('dwarf_number', number)
        self.value = 0


class Memory():
    def __init__(self, label: str, **kwargs):
        self.label = label
        self.width = kwargs.get('width')
        self._byte_memory = dict()

    def read(self, bits: int, addr: int):
        if bits % 8 == 0:
            value = 0
            for bi in range(bits // 8):
                # TODO: Memory should return X value if not initialized?
                if bi in self._byte_memory:
                    value += self._byte_memory[addr + bi] << (bi * 8)
                else:
                    value += 0
            return value
        raise ValueError()

    def write(self, bits: int, addr: int, value):
        if bits % 8 == 0:
            for bi in range(bits // 8):
                self._byte_memory[addr + bi] = value & 0xff
                value = value >> 8
            return
        raise ValueError()


class Immediate():
    def __init__(self, label: str, **kwargs):
        self.label = label
        self.width = kwargs.get('width')

    def cast(self, value):
        return value


class ImmU(Immediate):
    pass


class ImmS(Immediate):
    def __init__(self, label: str, **kwargs):
        super().__init__(label, **kwargs)

    def signed(self, value):
        if value & (1 << (self.width - 1)):
            value = value - (1 << self.width)
        return value

    def cast(self, value):
        return self.signed(value)


class Instruction():
    opc = None
    opn = None
    prm = None
    asm = None
    bin = None

    # Only one of jump, branch, call, tail or return can be True.
    is_jump = False
    is_branch = False
    is_call = False
    is_tail = False
    is_return = False

    is_indirect = False

    is_load = False
    is_store = False
    is_pop = False
    is_push = False

    has_sideeffect = False

    def __init__(self):
        self.isa = None
        self.addr = None
        self.params = InstructionParameters()
        self._operands = dict()
        self._pseudo_instrs = list()
        self._disasm_str = str()

    def __repr__(self):
        s = "Instruction({})"
        indent = ""
        prms = " ".join([
            indent + repr(self.opn),
            indent + repr(self.params.outputs),
            indent + repr(self.params.inputs),
        ])
        return s.format(prms)

    def __getattr__(self, key):
        if isinstance(key, str):
            param = None
            if key in self.params.inputs:
                param = self.params.inputs[key]
            elif key in self.params.outputs:
                param = self.params.outputs[key]
            if param:
                if self.isa.is_reg_type(param.type_):
                    return param.number
                elif self.isa.is_imm_type(param.type_):
                    return param.value
        return super().__getattr__(key)

    def __setattr__(self, key, value):
        if isinstance(key, str) and 'params' in self.__dict__ and key in self.params.outputs:
            self.params.outputs[key].value = value
            return
        super().__setattr__(key, value)

    def semantic(self, ctx, ins):
        pass

    def pipeline(self):
        pass

    @property
    def bitsize(self):
        if self.bin is None:
            return 0
        return self.bin.bitsize

    @property
    def bytesize(self):
        return self.bitsize // 8

    @property
    def opecode(self):
        return self.params.opecodes

    @property
    def operands(self):
        # return self.asm.operands
        if not self.isa:
            return None
        outlist = list()
        for ast in self.asm.ast:
            if ast == '$opn':
                opecode0 = list(self.params.opecodes.values())[0]
                outlist += [opecode0]
            elif ast[0] == '$':
                label = ast[1:]
                if label in self.params.outputs:
                    param = self.params.outputs[label]
                    outlist += [param]
                elif label in self.params.inputs:
                    param = self.params.inputs[label]
                    outlist += [param]
                else:
                    outlist += [InstructionParam()]
                    # raise ValueError()
            else:
                pass
        return outlist

    def target_addr(self):
        # jump/branch/call/tail target address
        # TODO: generate from semantic
        raise NotImplementedError()

    def match_opecode(self, value: int):
        bitvalue = 0
        for bits in reversed(self.bin.bitss):
            poped_value, value = bits.pop_value(value)
            if bits.label == "$opc":
                bitvalue += poped_value
        if bitvalue == self.opc:
            return True
        return False

    def decode(self, value: int, addr: int | None = None):
        if not self.isa:
            return None
        if not self.bin:
            return None
        self.addr = addr if addr is not None else 0
        self.params = InstructionParameters(isa=self.isa)
        for bits in reversed(self.bin.bitss):
            poped_value, value = bits.pop_value(value)
            if bits.label.startswith("$"):
                label = bits.label[1:]
                if label in self.prm.opecodes:
                    # key = 'opecodes'
                    tp = self.prm.opecodes[label]
                    self.params.opecodes.setdefault(label, self._make_param(label, tp))
                    param = self.params.opecodes[label]
                    self._add_value(param, tp, poped_value)
                if label in self.prm.outputs:
                    # key = 'outputs'
                    tp = self.prm.outputs[label]
                    self.params.outputs.setdefault(label, self._make_param(label, tp))
                    param = self.params.outputs[label]
                    self._add_value(param, tp, poped_value)
                if label in self.prm.inputs:
                    # key = 'inputs'
                    tp = self.prm.inputs[label]
                    self.params.inputs.setdefault(label, self._make_param(label, tp))
                    param = self.params.inputs[label]
                    self._add_value(param, tp, poped_value)
        for label, param in self.params.inputs.items():
            self._cast_value(param)

    def _make_param(self, label: str, tp: str):
        param = InstructionParam()
        param.instr = self
        param.label = label
        param.type_ = tp
        return param

    def _add_value(self, param, tp: str, poped_value: int):
        if self.isa.is_opc_type(tp):
            param.value = param.value if param.value is not None else 0
            param.value += poped_value
        elif self.isa.is_reg_type(tp):
            param.number = param.number if param.number is not None else 0
            param.number += poped_value
        elif self.isa.is_imm_type(tp):
            param.value = param.value if param.value is not None else 0
            param.value += poped_value
        # return param

    def _cast_value(self, param):
        for immtype in self.isa.immediates:
            if immtype.label == param.type_:
                param.value = immtype.cast(param.value)

    def disassemble(self):
        if not self.isa:
            return None
        isa = self.isa
        outstr = str()
        outparam = list()
        for ast in self.asm.ast:
            if ast == '$opn':
                outstr += self.opn
                outparam += [self.opn]
            elif ast[0] == '$':
                label = ast[1:]
                if label in self.params.outputs:
                    param = self.params.outputs[label]
                    outstr += isa.param_str(param)
                    outparam += [param]
                elif label in self.params.inputs:
                    param = self.params.inputs[label]
                    outstr += isa.param_str(param)
                    outparam += [param]
                else:
                    outstr += ast
                    outparam += [ast]
            else:
                outstr += ast
                outparam += [ast]
        self._disasm_str = outstr
        self._disasm_param = outparam
        return outstr


class unknown_op(Instruction):
    opn = "unknown_op"


class InstructionParameters():
    def __init__(self, isa=None):
        self.opecodes = InstructionParamDict(isa=isa)
        self.outputs = InstructionParamDict(isa=isa)
        self.inputs = InstructionParamDict(isa=isa)


class InstructionParamDict(dict):
    def __init__(self, *args, **kwargs):
        isa = kwargs.pop('isa')
        super().__init__(*args, **kwargs)
        self.isa = isa

    @property
    def regs(self):
        regs = list()
        for param in self.values():
            if self.isa.is_reg_type(param.type_):
                regs.append(param)
        return regs


class InstructionParam():
    def __init__(self):
        self.instr = None
        self.label = str()
        self.type_ = str()
        self.number = None
        self.value = None
        self.is_input = False
        self.is_output = False
        self.dataflow_src = None

    def __repr__(self):
        return "{}:{}=<{},{}>".format(
            self.label,
            self.type_,
            self.number,
            self.value,
        )

    def is_opc(self, isa):
        pass

    def is_reg(self, isa):
        pass

    def is_imm(self, isa):
        pass

    def is_symbol(self, isa):
        pass


class InstructionAssembly():
    def __init__(self, ptn: str):
        self.pattern = ptn
        self.ast = self.make_ast(ptn)

    def make_ast(self, ptn: str):
        astptns = re.split(r"(\$\w+)", ptn)
        asts = list()
        for astptn in astptns:
            if astptn == '':
                continue
            asts.append(astptn)
        return asts

    @property
    def operands(self):
        return [x for x in self.ast if x[0] == "$"]


class InstructionBinary():
    def __init__(self, ptn: str):
        self.bitss = self.make_bits(ptn)

    def __repr__(self):
        return ', '.join([repr(b) for b in self.bitss])

    def make_bits(self, ptn: str):
        bitptns = re.split(r"\s*,\s*", ptn)
        bitss = list()
        for bitptn in bitptns:
            bitss.append(Bits(bitptn))
        return bitss

    @property
    def bitsize(self):
        if not self.bitss:
            return 0
        size = 0
        for bits in self.bitss:
            size += bits.msb - bits.lsb + 1
        return size


def parameter(outputs: str, inputs: str) -> list[tuple[str, str]]:
    params = InstructionParameters()
    params.opecodes['opc'] = "Opc"
    if outputs != "":
        args = re.split(r"\s*,\s*", outputs)
        for arg in args:
            if m := re.match(r"(\w+)\s*:\s*(\w+)", arg):
                label, type_ = m.groups()
                params.outputs[label] = type_
            else:
                raise ValueError("Parse Error: Instruction Parameter: {}".format(
                    outputs
                ))

    if inputs != "":
        args = re.split(r"\s*,\s*", inputs)
        for arg in args:
            if m := re.match(r"(\w+)\s*:\s*(\w+)", arg):
                label, type_ = m.groups()
                params.inputs[label] = type_
            else:
                raise ValueError("Parse Error: Instruction Parameter: {}".format(
                    inputs
                ))

    return params


def assembly(ptn: str):
    asmops = InstructionAssembly(ptn)
    return asmops


def binary(ptn: str):
    bits = InstructionBinary(ptn)
    return bits


# ---- Instruction semantic utility ----

def signed(bits: int, value: int):
    sign = (1 << (bits - 1)) & value
    if sign:
        value = value - (1 << bits)
    return value


def unsigned(bits: int, value: int):
    return value & (2 ** bits - 1)


def s32(value: int):
    return signed(32, value)


def u32(value: int):
    return unsigned(32, value)
