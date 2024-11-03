import os
from jinja2 import Template


class Relocation():
    def __init__(self):
        pass


class KwargsClass():
    keys = ()

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class RegisterDef(KwargsClass):
    keys = (
        'varname',
        'no',
        'name',
        'aliases',
        'dwarfno',
    )

class RegisterClassDef(KwargsClass):
    keys = (
        'varname',
        'reg_varnames',
    )

class OperandCls(KwargsClass):
    keys = (
        'varname',
        'basecls',
    )

class OperandType(KwargsClass):
    keys = (
        'varname',
        'basecls',
    )

class InstrDefs(KwargsClass):
    keys = (
        'varname',
        'outs',
        'ins',
        'asmstr',
        'pattern',
        'bit_defs',
        'bit_insts',
        'attrs',
    )


instr_attr_table = {
    'is_return': ("isReturn", "isTerminator"),
    'is_jump': ("isBranch", "isTerminator"),
    'is_branch': ("isBranch", "isTerminator"),
    'is_indirect': ("isIndirectBranch", "isTerminator"),
    # '': "isCompare",
    # '': "isMoveImm",
    # '': "isMoveReg",
    # '': "isBitcast",
    # '': "isSelect",
    # '': "isBarrier",
    'is_call': ("isCall", "isBarrier"),
    # '': "isAdd",
    # '': "isTrap",
    'is_load': "mayLoad",
    'is_push': "mayLoad",
    'is_store': "mayStore",
    'is_pop': "mayStore",
    # '': "isTerminator",
}


class LLVMCompiler():
    namespace = "XXPU"

    def __init__(self, isa):
        self.isa = isa
        self.outdir = "out"

    @property
    def template_dir(self):
        return os.path.join(os.path.dirname(__file__),
                            "template", "llvm/llvm/lib/Target/Xpu")

    def gen_registerinfo_td(self):
        isa = self.isa

        reg_defs = []
        for reggroup in isa.registers:
            for reg in reggroup:
                reg_defs.append(RegisterDef(
                    namespace=self.namespace,
                    varname=reg.label.upper(),
                    no=reg.number,
                    name=reg.label,
                    aliases="[{}]".format(",".join('"{}"'.format(n) for n in reg.aliases)),
                    dwarfno=reg.dwarf_number,
                ))

        regcls_defs = []
        for reggroup in isa.registers:
            regcls_defs.append(RegisterClassDef(
                varname=reggroup.label,
                reg_varnames=','.join([reg.label.upper() for reg in reggroup]),
            ))

        template_fname = "XpuRegisterInfo.td"
        template_fpath = os.path.join(self.template_dir, template_fname)
        with open(template_fpath) as f:
            template_str = f.read()
        final_text = Template(source=template_str).render(
            namespace=self.namespace,
            reg_defs=reg_defs,
            regcls_defs=regcls_defs,
        )

        fname = f"{self.namespace}RegisterInfo.td"
        fpath = os.path.join(self.outdir, fname)
        os.makedirs(self.outdir, exist_ok=True)
        with open(fpath, "w") as f:
            f.write(final_text)

    def gen_instrinfo_td(self):
        isa = self.isa
        operand_clss = []
        operand_types = []
        for imm in isa.immediates:
            operand_clss.append(OperandCls(
                varname=imm.label,
                basecls="i32",
            ))
            operand_types.append(OperandType(
                varname=imm.label + "Tp",
                basecls="i32",
            ))
        for mem in isa.memories:
            operand_clss.append(OperandCls(
                varname=mem.label,
                basecls="i32",
            ))
            operand_types.append(OperandType(
                varname=mem.label + "Tp",
                basecls="i32",
            ))

        instr_defs = []
        for cls in isa.instructions:
            instr = cls()
            instr_def = InstrDefs()

            instr_def.varname = instr.__class__.__name__.upper()
            instr_def.outs = ', '.join([
                '{}:${}'.format(cls, label) for label, cls in instr.prm.outputs.items()
            ])
            instr_def.ins = ', '.join([
                '{}:${}'.format(cls, label) for label, cls in instr.prm.inputs.items()
            ])

            asmstrs = []
            for ast in instr.asm.ast:
                if ast == '$opn':
                    asmstrs += [instr.opn]
                elif ast[0] == "$":
                    asmstrs += ["${{{}}}".format(ast[1:])]
                else:
                    asmstrs += [ast]
            instr_def.asmstr = '"{}"'.format(''.join(asmstrs))

            instr_def.pattern = "[]"

            bit_defs = []
            bit_instrs = []
            bit_sum = 0
            for bits in reversed(instr.bin.bitss):
                if bits.label == "$opc":
                    bits_value = (instr.opc >> bit_sum) & (2 ** (bits.msb - bits.lsb) - 1)
                    bit_instrs.append("  let Inst{{{}-{}}} = {};".format(
                        bit_sum + bits.msb - bits.lsb,
                        bit_sum,
                        bits_value,
                    ))
                else:
                    bit_defs.append("  bits<{}> {};".format(
                        bits.size(),
                        bits.label[1:],
                    ))
                    bit_instrs.append("  let Inst{{{}-{}}} = {};".format(
                        bit_sum + bits.msb,
                        bit_sum,
                        bits.label[1:],
                    ))
                bit_sum += bits.msb - bits.lsb + 1
            instr_def.bit_defs = "\n".join(bit_defs)
            instr_def.bit_insts = "\n".join(bit_instrs)

            attrs = []
            for k, v in instr_attr_table.items():
                if not hasattr(instr, k):
                    continue
                if getattr(instr, k) is True:
                    if isinstance(v, str):
                        v = [v]
                    attrs += v
            attrs = list(set(attrs))
            attrs = [f"  let {x} = true;"for x in attrs]
            instr_def.attrs = "\n".join(attrs)

            instr_defs.append(instr_def)

        template_fname = "XpuInstrInfo.td"
        template_fpath = os.path.join(self.template_dir, template_fname)
        with open(template_fpath) as f:
            template_str = f.read()
        final_text = Template(source=template_str).render(
            namespace=self.namespace,
            operand_clss=operand_clss,
            operand_types=operand_types,
            instr_defs=instr_defs,
        )

        out_fname = f"{self.namespace}InstrInfo.td"
        out_fpath = os.path.join(self.outdir, out_fname)
        os.makedirs(self.outdir, exist_ok=True)
        with open(out_fpath, "w") as f:
            f.write(final_text)
