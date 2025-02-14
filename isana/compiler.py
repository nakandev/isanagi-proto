import os
import re
from jinja2 import Template
from isana.semantic import (
    may_change_pc_absolute,
    may_change_pc_relative,
    may_take_memory_address,
    get_alu_dag,
    get_alui_dag,
    get_cmp_dag,
    get_cmpi_dag,
)


_default_namespace = "Xpu"
_default_triple = ("xpu", "", "")


class KwargsClass():
    keys = ()

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class RegisterBase(KwargsClass):
    keys = (
        'name',
        'bitsize',
    )


class RegisterDef(KwargsClass):
    keys = (
        'varname',
        'basename',
        'no',
        'name',
        'aliases',
        'dwarfno',
    )

class RegisterClassDef(KwargsClass):
    keys = (
        'varname',
        'regs',
        'reg_varnames',
        'bitsize',
    )

class AsmOperandCls(KwargsClass):
    keys = (
        'name',
        'enums',
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
        'cond',
    )

class InstrDefs(KwargsClass):
    keys = (
        'varname',
        'outs',
        'ins',
        'asmstr',
        'pattern',
        'params',
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
    'is_pop': "mayLoad",
    'is_store': "mayStore",
    'is_push': "mayStore",
    # '': "isTerminator",
}


class Fixup(KwargsClass):
    keys = (
        'namespace',
        'number',
        'name_enum',
        'addend',
        'bin',
        'offset',
        'size',
        'flags',
        'reloc_procs',
    )

    def __init__(self, **kwargs):
        self.namespace = kwargs.pop('namespace', _default_namespace)
        self.number = kwargs.pop('number', -1)
        self.name = kwargs.pop('name', str())
        self.addend = kwargs.pop('addend', None)
        self.bin = kwargs.pop('bin', None)
        self.name_enum = f"fixup_{self.namespace.lower()}_{self.name}"
        self.reloc_procs = list()
        super().__init__(**kwargs)


def auto_make_fixups(isa):
    fixups = list()
    fixups += auto_make_relocations(isa)
    return fixups


def auto_make_relocations(isa):
    relocs = {
        "pc_abs": list(),
        "pc_rel": list(),
        "mem_addr": list(),
        "other_imm": list(),
    }
    instrs = dict()
    for cls in isa.instructions:
        if not hasattr(cls, 'semantic'):
            continue
        instr = cls()
        bin_filtered = re.sub(r"\$(?!opc|imm)\w+", r"$_", str(instr.bin))
        relocinfo = (instr.bitsize, bin_filtered)
        if may_change_pc_absolute(instr.semantic):
            key = "pc_abs"
            relocs[key].append(relocinfo)
            instrs.setdefault((key, bin_filtered), list())
            instrs[(key, bin_filtered)].append(cls)
        elif may_change_pc_relative(instr.semantic):
            key = "pc_rel"
            relocs[key].append(relocinfo)
            instrs.setdefault((key, bin_filtered), list())
            instrs[(key, bin_filtered)].append(cls)
        elif may_take_memory_address(instr.semantic):
            key = "mem_addr"
            relocs[key].append(relocinfo)
            instrs.setdefault((key, bin_filtered), list())
            instrs[(key, bin_filtered)].append(cls)
        elif "imm" in instr.prm.inputs.keys():  # TODO fix condition
            key = "other_imm"
            relocs[key].append(relocinfo)
            instrs.setdefault((key, bin_filtered), list())
            instrs[(key, bin_filtered)].append(cls)
        else:
            pass
    fixups = list()
    fixups += [
        Fixup(name="32", offset=0, size=32, flags=0, bin=32),
        Fixup(name="64", offset=0, size=64, flags=0, bin=64),
    ]
    for key in relocs:
        relocs[key] = sorted(list(set(relocs[key])), key=lambda x: str(x[1]))
        for ri, info in enumerate(relocs[key]):
            bitsize, bin_ = info
            fixup = Fixup()
            fixup.name = f"{key}_{ri}"
            fixup.offset = 0
            fixup.size = bitsize  # TODO: fix it
            if key == "pc_rel":
                fixup.flags = "MCFixupKindInfo::FKF_IsPCRel"
            else:
                fixup.flags = "0"  # TODO: fix it
            fixup.bin = bin_
            fixup.instrs = [i() for i in sorted(list(set(instrs[(key, bin_)])), key=lambda x: x.opn)]
            fixups.append(fixup)
    instr_reloc_table = dict()

    for fixup in fixups:
        procs = list()
        if fixup.bin is None:
            pass
        if isinstance(fixup.bin, int):
            procs.append("  | val")
        else:
            bit_sum = 0
            for bits in reversed(fixup.instrs[0].bin.bitss):
                if bits.label == "$imm":
                    procs.append("  | (((val >> {}) & {}) << {})".format(
                        bits.lsb,
                        2 ** bits.size() - 1,
                        bit_sum,
                    ))
                bit_sum += bits.size()
        fixup.reloc_procs = procs
        if fixup in instr_reloc_table.keys():
            fixup.instrs = instr_reloc_table[fixup]
    return fixups


def get_instr_pattern(instr):
    if ret := get_alu_dag(instr.semantic):
        (op, (dst_name, dst_tp), (l_name, l_tp), (r_name, r_tp)) = ret
        s = "[(set {}, ({} {}, {}))]".format(
            "{}:${}".format(dst_tp, dst_name),
            op,  # get_basic_operator(instr.opn)
            "{}:${}".format(l_tp, l_name),
            "{}:${}".format(r_tp, r_name),
        )
        return s
    elif ret := get_alui_dag(instr.semantic):
        s = "[(set {}, ({} {}, {}))]".format(
            "{}:${}".format(dst_tp, dst_name),
            op,  # get_basic_operator(instr.opn)
            "{}:${}".format(l_tp, l_name),
            "{}:${}".format(r_tp, r_name),
        )
        return s
        pass
    elif ret := get_cmp_dag(instr.semantic):
        pass
    elif ret := get_cmpi_dag(instr.semantic):
        pass
    return "[]"


class LLVMCompiler():
    namespace = _default_namespace
    triple = tuple(_default_triple)
    fixups = tuple()

    def __init__(self, isa):
        self.isa = isa
        self.outdir = "out"
        self._init_fixups()

    @property
    def template_dir(self):
        return os.path.join(os.path.dirname(__file__), "template", "llvm")

    def _init_fixups(self):
        if len(self.fixups) > 0:
            fixups = self.fixups[:]
        else:
            fixups = auto_make_fixups(self.isa)
        for fixup in fixups:
            fixup.namespace = self.namespace
            fixup.name_enum = f"fixup_{fixup.namespace.lower()}_{fixup.name}"
        self._fixups = fixups

    def _read_template_and_write(self, fdirs, fname, tmp_kwargs):
        fprefix, fname = fname
        template_fdir = os.path.join(self.template_dir, *fdirs)
        template_fname = f"{fprefix}{fname}"
        template_fpath = os.path.join(template_fdir, template_fname)
        with open(template_fpath) as f:
            template_str = f.read()
        final_text = Template(source=template_str).render(
            **tmp_kwargs,
        )

        out_fdirs = [d.replace(f"{_default_namespace}", f"{self.namespace}") for d in fdirs]
        out_fdir = os.path.join(self.outdir, *out_fdirs)
        out_fname = "{}{}".format(
            f"{fprefix}".replace(f"{_default_namespace}", f"{self.namespace}"),
            f"{fname}")
        out_fpath = os.path.join(out_fdir, out_fname)
        os.makedirs(out_fdir, exist_ok=True)
        with open(out_fpath, "w") as f:
            f.write(final_text)

    def gen_lld_elf_arch_xpu_cpp(self):
        fixups = self._fixups
        fixup_relocs = fixups[:]

        fdirs = "lld/ELF/Arch".split("/")
        fname = "Xpu", ".cpp"
        kwargs = {
            "namespace": self.namespace,
            "fixup_relocs": fixup_relocs,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_elfrelocs_xpu_def(self):
        fixups = self._fixups

        fdirs = "llvm/include/llvm/BinaryFormat/ELFRelocs".split("/")
        fname = "Xpu", ".def"
        kwargs = {
            "namespace": self.namespace,
            "fixups": fixups,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_callingconv_td(self):
        callee_saved_regs = []
        arg_regs = []
        ret_regs = []
        gpr = next(filter(lambda rg: rg.label == "GPR", self.isa.registers), None)
        if gpr:
            regs = list(filter(lambda r: r.is_callee_saved, gpr.regs))
            callee_saved_regs = ', '.join([r.label.upper() for r in regs])
            regs = list(filter(lambda r: r.is_arg, gpr.regs))
            arg_regs = ', '.join([r.label.upper() for r in regs])
            regs = list(filter(lambda r: r.is_ret, gpr.regs))
            ret_regs = ', '.join([r.label.upper() for r in regs])

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "CallingConv.td"
        kwargs = {
            "namespace": self.namespace,
            "callee_saved_regs": callee_saved_regs,
            "arg_regs": arg_regs,
            "ret_regs": ret_regs,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_registerinfo_td(self):
        reg_base_tables = {}
        for reggroup in self.isa.registers:
            for reg in reggroup:
                reg_clsname = reg.__class__.__name__
                reg_base_tables.setdefault(reg_clsname, list())
                reg_base_tables[reg_clsname].append(reg)
        reg_bases = []
        for name, regs in reg_base_tables.items():
            if name == "Register":
                continue
            max_no = max([r.number for r in regs])
            reg_bases.append(RegisterBase(
                name=name,
                bitsize=max_no.bit_length(),
            ))

        reg_defs = []
        reg_labels = []
        for reggroup in self.isa.registers:
            if reggroup.label == "PCR":
                continue
            for reg in reggroup:
                if reg.label in reg_labels:
                    continue
                reg_labels.append(reg.label)
                reg_defs.append(RegisterDef(
                    namespace=self.namespace,
                    varname=reg.label.upper(),
                    basename=reg.__class__.__name__,
                    no=reg.number,
                    name=reg.label,
                    aliases="[{}]".format(",".join('"{}"'.format(n) for n in reg.aliases)),
                    dwarfno=reg.dwarf_number,
                ))

        regcls_defs = []
        for reggroup in self.isa.registers:
            if reggroup.label == "PCR":
                continue
            regcls_defs.append(RegisterClassDef(
                varname=reggroup.label,
                reg_varnames=','.join([reg.label.upper() for reg in reggroup]),
                bitsize=int(len(reggroup.regs) - 1).bit_length(),
            ))

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "RegisterInfo.td"
        kwargs = {
            "namespace": self.namespace,
            "reg_bases": reg_bases,
            "reg_defs": reg_defs,
            "regcls_defs": regcls_defs,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_registerinfo_cpp(self):
        reserved_regs = []
        gpr = next(filter(lambda rg: rg.label == "GPR", self.isa.registers), None)
        reg0 = None
        sp = None
        fp = None
        if gpr:
            reg0 = gpr.regs[0].label.upper()
            for reg in gpr.regs:
                if any([
                    reg.is_zero, reg.is_return_address, reg.is_stack_pointer, reg.is_global_pointer,
                ]):
                    reserved_regs.append(reg.label.upper())
                if sp is None and (reg.is_stack_pointer):
                    sp = reg.label.upper()
                if fp is None and (reg.is_frame_pointer):
                    fp = reg.label.upper()

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "RegisterInfo.cpp"
        kwargs = {
            "namespace": self.namespace,
            "reserved_regs": reserved_regs,
            "reg0": reg0,
            "sp": sp,
            "fp": fp,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_registerinfo_h(self):
        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "RegisterInfo.h"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_instrinfo_td(self):
        asm_operand_clss = []
        operand_clss = []
        operand_types = []
        for imm in self.isa.immediates:
            operand_cls = OperandCls(
                varname=imm.label,
                basecls="i32",
            )
            if isinstance(imm.enums, dict):
                asm_operand_cls = AsmOperandCls(
                    name=imm.label,
                    enums=imm.enums,
                )
                asm_operand_clss.append(asm_operand_cls)
                operand_cls.asm_operand_cls = asm_operand_cls
                operand_cls.imm_leaf = None
            else:
                operand_cls.asm_operand_cls = None
                cond = "return ({minv} <= (Imm>>{shift})) && ((Imm>>{shift}) <= {maxv});".format(
                    shift=imm.offset,
                    minv=-int(pow(2, imm.width)),
                    maxv=int(pow(2, imm.width) - 1),
                )
                operand_cls.imm_leaf = OperandType(
                    varname=imm.label + "Tp",
                    basecls="i32",
                    cond=cond,
                )
            operand_clss.append(operand_cls)
        for mem in self.isa.memories:
            operand_clss.append(OperandCls(
                varname=mem.label,
                basecls="i32",
            ))

        instr_defs = []
        for cls in self.isa.instructions:
            instr = cls()
            instr_def = InstrDefs()

            instr_def.varname = instr.__class__.__name__.upper()
            instr_def.ins = ', '.join([
                '{}:${}'.format(cls, label) for label, cls in instr.prm.inputs.items()
            ])

            # instr_def.outs = ', '.join([
            #     '{}:${}'.format(cls, label) for label, cls in instr.prm.outputs.items()
            # ])
            instr_def.outs = []
            duplicated_outs = {}
            for label, cls in instr.prm.outputs.items():
                if label in instr.prm.inputs.keys():
                    new_label = label + "_o"
                    duplicated_outs[label] = new_label
                    label = new_label
                instr_def.outs.append('{}:${}'.format(cls, label))
            instr_def.outs = ", ".join(instr_def.outs)

            asmstrs = []
            for ast in instr.asm.ast:
                if ast == '$opn':
                    asmstrs += [instr.opn]
                elif ast[0] == "$":
                    asmstrs += ["${{{}}}".format(ast[1:])]
                else:
                    asmstrs += [ast]
            instr_def.asmstr = '"{}"'.format(''.join(asmstrs))

            instr_def.pattern = get_instr_pattern(instr)

            params = []
            # params.append("  let DecoderNamespace = \"{}\";".format(
            #     f"{self.namespace}{instr.bitsize}",
            # ))
            params.append("  let Size = {};".format(
                instr.bytesize,
            ))
            if duplicated_outs:
                params.append("  let Constraints = \"{}\";".format(','.join(
                    ["${} = ${}".format(
                        il, ol,
                    ) for il, ol in duplicated_outs.items()]
                )))
            params = "\n".join(params)
            instr_def.params = params

            bitss_by_name = dict()
            for bits in instr.bin.bitss:
                bitss_by_name.setdefault(bits.label, list())
                bitss_by_name[bits.label].append(bits)

            bit_defs = []
            bit_instrs = []
            for label, bitss in reversed(bitss_by_name.items()):
                if label == "$opc":
                    pass
                else:
                    bitss_size = sum([b.size() for b in bitss])
                    bit_defs.append("  bits<{}> {};".format(
                        bitss_size,
                        label[1:],
                    ))
                bit_sum = 0
                for bits in reversed(bitss):
                    if bits.label == "$opc":
                        # bits_value = (instr.opc >> bit_sum) & (2 ** (bits.msb - bits.lsb) - 1)
                        bits_value = (instr.opc >> bits.offset) & (2 ** (bits.size()) - 1)
                        let_str = ""
                        if bits.size() == 1:
                            let_str += "  let Inst{{{}}} = ".format(bits.offset)
                        else:
                            let_str += "  let Inst{{{}-{}}} = ".format(
                                bits.offset + bits.size() - 1,
                                bits.offset,
                            )
                        let_str += "{};".format(bits_value)
                        bit_instrs.append(let_str)
                    else:
                        let_str = ""
                        if bits.size() == 1:
                            let_str += "  let Inst{{{}}} = ".format(bits.offset)
                        else:
                            let_str += "  let Inst{{{}-{}}} = ".format(
                                bits.offset + bits.size() - 1,
                                bits.offset,
                            )
                        if bits.size() == 1:
                            let_str += "{}{{{}}};".format(bits.label[1:], bit_sum)
                        else:
                            let_str += "{}{{{}-{}}};".format(
                                bits.label[1:],
                                bit_sum + bits.size() - 1,
                                bit_sum,
                            )
                        # bit_instrs.append("  let Inst{{{}-{}}} = {}{{{}-{}}};".format(
                        #     bits.offset + bits.size() - 1,
                        #     bits.offset,
                        #     bits.label[1:],
                        #     bit_sum + bits.size() - 1,
                        #     bit_sum,
                        # ))
                        bit_instrs.append(let_str)
                    bit_sum += bits.size()
            # for bits in reversed(instr.bin.bitss):
            #     if bits.label == "$opc":
            #         bits_value = (instr.opc >> bit_sum) & (2 ** (bits.msb - bits.lsb) - 1)
            #         bit_instrs.append("  let Inst{{{}-{}}} = {};".format(
            #             bit_sum + bits.msb - bits.lsb,
            #             bit_sum,
            #             bits_value,
            #         ))
            #     else:
            #         bit_defs.append("  bits<{}> {};".format(
            #             bits.size(),
            #             bits.label[1:],
            #         ))
            #         bit_instrs.append("  let Inst{{{}-{}}} = {};".format(
            #             bit_sum + bits.msb - bits.lsb,
            #             bit_sum,
            #             bits.label[1:],
            #         ))
            #     bit_sum += bits.size()
            instr_def.bit_defs = "\n".join(bit_defs)
            instr_def.bit_insts = "\n".join(bit_instrs)

            attrs = []
            instr_attrs = [f for f in dir(instr)]
            for k, v in instr_attr_table.items():
                # if not hasattr(instr, k):
                if k not in instr_attrs:
                    continue
                try:
                    cond = getattr(instr, k) is True
                except Exception:
                    # if instr_attr is a method, set attr forcely as trial.
                    cond = True
                if cond:
                    if isinstance(v, str):
                        v = [v]
                    attrs += v
            attrs = list(set(attrs))
            attrs = [f"  let {x} = true;"for x in attrs]
            instr_def.attrs = "\n".join(attrs)

            instr_defs.append(instr_def)

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "InstrInfo.td"
        kwargs = {
            "namespace": self.namespace,
            "asm_operand_clss": asm_operand_clss,
            "operand_clss": operand_clss,
            "operand_types": operand_types,
            "instr_defs": instr_defs,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_instrinfo_cpp(self):
        pass

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "InstrInfo.cpp"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_instrinfo_h(self):
        pass

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "InstrInfo.h"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_framelowering_cpp(self):
        pass
        gpr = next(filter(lambda rg: rg.label == "GPR", self.isa.registers), None)
        sp = None
        if gpr:
            for reg in gpr.regs:
                if sp is None and (reg.is_stack_pointer):
                    sp = reg.label.upper()

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "FrameLowering.cpp"
        kwargs = {
            "namespace": self.namespace,
            "sp": sp,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_framelowering_h(self):
        pass

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "FrameLowering.h"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_isellowering_cpp(self):
        pass

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "ISelLowering.cpp"
        kwargs = {
            "namespace": self.namespace,
            # "asm_operand_clss": asm_operand_clss,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_isellowering_h(self):
        pass

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "ISelLowering.h"
        kwargs = {
            "namespace": self.namespace,
            # "asm_operand_clss": asm_operand_clss,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_iseldagtodag_cpp(self):
        pass

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "ISelDAGToDAG.cpp"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_iseldagtodag_h(self):
        pass

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "ISelDAGToDAG.h"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_subtarget_cpp(self):
        pass

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "Subtarget.cpp"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_subtarget_h(self):
        pass

        fdirs = f"llvm/lib/Target/{_default_namespace}".split("/")
        fname = "Xpu", "Subtarget.h"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_asmbackend_h(self):
        fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "Xpu", "AsmBackend.h"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_asmbackend_cpp(self):
        fixups = self._fixups
        fixups_should_force_reloc = list()
        fixups_adjust = fixups[:]
        relax_instrs = list()

        fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "Xpu", "AsmBackend.cpp"
        kwargs = {
            "namespace": self.namespace,
            "fixups": fixups,
            "fixups_should_force_reloc": fixups_should_force_reloc,
            "fixups_adjust": fixups_adjust,
            "relax_instrs": relax_instrs,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_elfobjectwriter_cpp(self):
        fixups = self._fixups
        fixups_pc_rel = [fx for fx in fixups if fx.name[:6] == "pc_rel"]
        fixup_relocs = [fx for fx in fixups if not isinstance(fx.bin, int)]

        fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "Xpu", "ELFObjectWriter.cpp"
        kwargs = {
            "namespace": self.namespace,
            "fixups_pc_rel": fixups_pc_rel,
            "fixup_relocs": fixup_relocs,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_fixupkinds_h(self):
        fixups = self._fixups

        fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "Xpu", "FixupKinds.h"
        kwargs = {
            "namespace": self.namespace,
            "fixups": fixups,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_instprinter_cpp(self):
        asm_operand_clss = []
        for imm in self.isa.immediates:
            if isinstance(imm.enums, dict):
                asm_operand_cls = AsmOperandCls(
                    name=imm.label,
                    enums=imm.enums,
                )
                asm_operand_clss.append(asm_operand_cls)

        fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "Xpu", "InstPrinter.cpp"
        kwargs = {
            "namespace": self.namespace,
            "asm_operand_clss": asm_operand_clss,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_instprinter_h(self):
        asm_operand_clss = []
        for imm in self.isa.immediates:
            if isinstance(imm.enums, dict):
                asm_operand_cls = AsmOperandCls(
                    name=imm.label,
                    enums=imm.enums,
                )
                asm_operand_clss.append(asm_operand_cls)

        fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "Xpu", "InstPrinter.h"
        kwargs = {
            "namespace": self.namespace,
            "asm_operand_clss": asm_operand_clss,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_mcasminfo_cpp(self):
        fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "Xpu", "MCAsmInfo.cpp"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_mcasminfo_h(self):
        fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "Xpu", "MCAsmInfo.h"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_mccodeemitter_cpp(self):
        fixups = self._fixups
        fixup_relocs = [fx for fx in fixups if not isinstance(fx.bin, int)]

        fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "Xpu", "MCCodeEmitter.cpp"
        kwargs = {
            "namespace": self.namespace,
            "fixup_relocs": fixup_relocs,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_mcexpr_cpp(self):
        fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "Xpu", "MCExpr.cpp"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_mcexpr_h(self):
        fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "Xpu", "MCExpr.h"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_cmakelists_txt(self, fdirs):
        # fdirs = f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/")
        fname = "", "CMakeLists.txt"
        kwargs = {
            "namespace": self.namespace,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_asmparser_cpp(self):
        asm_operand_clss = []
        for imm in self.isa.immediates:
            if isinstance(imm.enums, dict):
                asm_operand_cls = AsmOperandCls(
                    name=imm.label,
                    enums=imm.enums,
                )
                asm_operand_clss.append(asm_operand_cls)

        fdirs = f"llvm/lib/Target/{_default_namespace}/AsmParser".split("/")
        fname = "Xpu", "AsmParser.cpp"
        kwargs = {
            "namespace": self.namespace,
            "asm_operand_clss": asm_operand_clss,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_asmparser_dir(self):
        self.gen_cmakelists_txt(f"llvm/lib/Target/{_default_namespace}/AsmParser".split("/"))
        self.gen_asmparser_cpp()

    def gen_disassembler_cpp(self):

        def reg_varname(reg, reggroup):
            if reggroup.label == "GPR":
                return reg.label.upper()
            else:
                return "{}_{}".format(reg.label, reggroup.label).upper()

        instr_bitsizes = list(set([ins().bitsize for ins in self.isa.instructions]))

        regcls_defs = []
        for reggroup in self.isa.registers:
            if reggroup.label == "PCR":
                continue
            reg_varnames = ["{}::{}".format(
                self.namespace, reg.label.upper()) for reg in reggroup]
            reg_varnames = ',\n'.join(reg_varnames)
            regcls_defs.append(RegisterClassDef(
                varname=reggroup.label,
                regs=reggroup.regs,
                # reg_varnames=','.join([reg.label.upper() for reg in reggroup]),
                # reg_varnames=','.join([reg_varname(reg, reggroup) for reg in reggroup]),
                reg_varnames=reg_varnames,
                bitsize=int(len(reggroup.regs) - 1).bit_length(),
            ))

        fdirs = f"llvm/lib/Target/{_default_namespace}/Disassembler".split("/")
        fname = "Xpu", "Disassembler.cpp"
        kwargs = {
            "namespace": self.namespace,
            # "gpr_regs": gpr_regs,
            "instr_bitsizes": instr_bitsizes,
            "regcls_defs": regcls_defs,
        }
        self._read_template_and_write(fdirs, fname, kwargs)

    def gen_disassembler_dir(self):
        self.gen_cmakelists_txt(f"llvm/lib/Target/{_default_namespace}/Disassembler".split("/"))
        self.gen_disassembler_cpp()

    def gen_mctargetdesc_dir(self):
        self.gen_cmakelists_txt(f"llvm/lib/Target/{_default_namespace}/MCTargetDesc".split("/"))
        self.gen_asmbackend_cpp()
        self.gen_asmbackend_h()
        self.gen_asmbackend_cpp()
        self.gen_elfobjectwriter_cpp()
        self.gen_fixupkinds_h()
        self.gen_instprinter_cpp()
        self.gen_instprinter_h()
        self.gen_mcasminfo_cpp()
        self.gen_mcasminfo_h()
        self.gen_mccodeemitter_cpp()
        self.gen_mcexpr_cpp()
        self.gen_mcexpr_h()

    def gen_llvm_lib_target(self):
        self.gen_lld_elf_arch_xpu_cpp()

        self.gen_elfrelocs_xpu_def()

        self.gen_asmparser_dir()
        self.gen_disassembler_dir()
        self.gen_mctargetdesc_dir()
        self.gen_callingconv_td()
        self.gen_framelowering_cpp()
        self.gen_framelowering_h()
        self.gen_instrinfo_cpp()
        self.gen_instrinfo_h()
        self.gen_instrinfo_td()
        self.gen_iseldagtodag_cpp()
        self.gen_iseldagtodag_h()
        self.gen_isellowering_cpp()
        self.gen_isellowering_h()
        self.gen_registerinfo_td()
        self.gen_registerinfo_cpp()
        self.gen_registerinfo_h()
        self.gen_subtarget_cpp()
        self.gen_subtarget_h()
