import os

# RegisterInfo.td
template_registerinfo_td = '''
//=== Registers
{reg_cls}

{reg_defs}

//=== Register Classes
{regcls_defs}
'''.strip('\n')

template_register_cls = '''
class CustomXPUReg<bits<16> Enc, string n, list<string> alt = []>: Register<n> {{
    let HWEncoding = Enc;
    let AltNames = alt;
    let Namespace = "{namespace}";
}}
'''.strip('\n')

template_register_def = '''
def {varname} : CustomXPUReg<{no}, "{name}", {aliases}>, DwarfRegNum<[{dwarfno}]>;
'''.strip('\n')
template_register_class_def = '''
def {rcname} : RegisterClass<"{namespace}", [i32], 32, (add
  {varnames}
)>;
'''.strip('\n')

# InstrInfo.td
template_instrinfo_td = '''
//=== Operands
{operand_cls}

//=== OperandTypes
{operand_types}

//=== Instruction Classes
{instr_cls}

//=== Instruction Defs
{instr_defs}

//=== Pseudo Instruction Defs
{instr_pseudo_call}
'''.strip('\n')

template_operand_cls = '''
def {varname}: Operand<{basecls}>;
'''.strip('\n')

template_operand_types = '''
def {varname} : IntImmLeaf<{basecls}, [{{return Imm == (Imm & 0xff);}}]>;
'''.strip('\n')

template_instruction_cls = '''
class CustomXPUInst<dag outs, dag ins, string asmstr, list<dag> pattern>: Instruction {{
  let Namespace = "{namespace}";
  field bits<32> Inst;
  let Size = 4;
  let OutOperandList = outs;
  let InOperandList  = ins;
  let AsmString   = asmstr;
  let Pattern     = pattern;
  let DecoderNamespace = "{namespace}";
  field bits<32> SoftFail = 0;
}}
'''.strip('\n')

template_instr_def = '''
def {varname}: CustomXPUInst<
  {outs}, {ins},
  {asmstr},
  {pattern}>
{{
{bits}
{instr_bits}
{attrs}
}}
'''.strip('\n')

template_instr_pseudo_call = '''
def customxpu_ret_glue : SDNode<
  "CustomXPUISD::RET_GLUE", SDTNone,
  [SDNPHasChain, SDNPOptInGlue, SDNPVariadic]>;

def PseudoRET: CustomXPUInst<
  (outs), (ins),
  "",
  [(customxpu_ret_glue)]>
{
  let isPseudo = 1;
  let isCodeGenOnly = 1;
  let isBarrier = 1;
  let isReturn = 1;
  let isTerminator = 1;
}
'''.strip('\n')


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


class Relocation():
    def __init__(self):
        pass


class LLVMCompiler():
    namespace = "XXPU"

    def __init__(self, isa):
        self.isa = isa
        self.outdir = "out"

    def gen_registerinfo_td(self):
        isa = self.isa
        reg_cls = template_register_cls.format(
            namespace=self.namespace,
        )

        reg_defs = []
        for reggroup in isa.registers:
            for reg in reggroup:
                reg_defs += [template_register_def.format(
                    namespace=self.namespace,
                    varname=reg.label.upper(),
                    no=reg.number,
                    name=reg.label,
                    aliases="[{}]".format(",".join('"{}"'.format(n) for n in reg.aliases)),
                    dwarfno=reg.dwarf_number,
                )]

        regcls_defs = []
        for reggroup in isa.registers:
            regcls_defs += [template_register_class_def.format(
                namespace=self.namespace,
                rcname=reggroup.label,
                varnames=','.join([reg.label.upper() for reg in reggroup]),
            )]

        final_text = template_registerinfo_td.format(
            reg_cls=reg_cls,
            reg_defs='\n'.join(reg_defs),
            regcls_defs='\n'.join(regcls_defs),
        )

        fname = f"{self.namespace}RegisterInfo.td"
        fpath = os.path.join(self.outdir, fname)
        os.makedirs(self.outdir, exist_ok=True)
        with open(fpath, "w") as f:
            f.write(final_text)

    def gen_instrinfo_td(self):
        isa = self.isa
        operand_cls = []
        for imm in isa.immediates:
            s = template_operand_cls.format(
                varname=imm.label,
                basecls="i32",
            )
            operand_cls.append(s)
        for mem in isa.memories:
            s = template_operand_cls.format(
                varname=mem.label,
                basecls="i32",
            )
            operand_cls.append(s)

        operand_types = []
        for imm in isa.immediates:
            s = template_operand_types.format(
                varname=imm.label + "Tp",
                basecls="i32",
            )
            operand_types.append(s)
        for mem in isa.memories:
            s = template_operand_types.format(
                varname=mem.label + "Tp",
                basecls="i32",
            )
            operand_types.append(s)

        instr_cls = template_instruction_cls.format(
            namespace=self.namespace,
        )

        instr_defs = []
        for cls in isa.instructions:
            instr = cls()
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

            asmstrs = []
            for ast in instr.asm.ast:
                if ast == '$opn':
                    asmstrs += [instr.opn]
                elif ast[0] == "$":
                    asmstrs += ["${{{}}}".format(ast[1:])]
                else:
                    asmstrs += [ast]
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
            instr_def = template_instr_def.format(
                varname=instr.__class__.__name__.upper(),
                outs="(outs {})".format(', '.join([
                    '{}:${}'.format(cls, label) for label, cls in instr.prm.outputs.items()
                ])),
                ins="(ins {})".format(', '.join([
                    '{}:${}'.format(cls, label) for label, cls in instr.prm.inputs.items()
                ])),
                # asmstr='"{}"'.format(''.join(instr.asm.ast).replace("$opn", instr.opn)),
                asmstr='"{}"'.format(''.join(asmstrs)),
                pattern="[]",
                bits="\n".join(bit_defs),
                instr_bits="\n".join(bit_instrs),
                attrs="\n".join(attrs),
            )
            instr_defs += [instr_def]

        instr_pseudo_call = template_instr_pseudo_call

        final_text = template_instrinfo_td.format(
            operand_cls="\n".join(operand_cls),
            operand_types="\n".join(operand_types),
            instr_cls=instr_cls,
            instr_defs="\n".join(instr_defs),
            instr_pseudo_call=instr_pseudo_call,
        )

        fname = f"{self.namespace}InstrInfo.td"
        fpath = os.path.join(self.outdir, fname)
        os.makedirs(self.outdir, exist_ok=True)
        with open(fpath, "w") as f:
            f.write(final_text)
