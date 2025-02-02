//=== AsmOperandClasses
{% for asmopcls in asm_operand_clss -%}
def {{ asmopcls.name }}AsmOp: AsmOperandClass {
  let Name = "{{ asmopcls.name }}AsmOp";
  let PredicateMethod = "isImm";
  let RenderMethod = "addImmOperands";
  let ParserMethod = "parse{{ asmopcls.name }}AsmOp";
}
{% endfor %}

//=== Operands
{% for opcls in operand_clss -%}
{% if opcls.asm_operand_cls -%}
def {{ opcls.varname }}: Operand<{{ opcls.basecls }}> {
  let ParserMatchClass = {{ opcls.asm_operand_cls.name }}AsmOp;
  let PrintMethod = "print{{ opcls.asm_operand_cls.name }}";
}
{% elif opcls.imm_leaf -%}
def {{ opcls.varname }}: Operand<{{ opcls.basecls }}>, ImmLeaf<{{ opcls.basecls }}, [{ {{ opcls.imm_leaf.cond }} }]>;
{% else -%}
def {{ opcls.varname }}: Operand<{{ opcls.basecls }}>;
{% endif -%}
{% endfor %}

//=== Instruction Classes
class {{ namespace }}Inst<dag outs, dag ins, string asmstr, list<dag> pattern>: Instruction {
  let Namespace = "{{ namespace }}";
  field bits<32> Inst;
  let Size = 4;
  let OutOperandList = outs;
  let InOperandList  = ins;
  let AsmString   = asmstr;
  let Pattern     = pattern;
  let DecoderNamespace = "{{ namespace }}";
  field bits<32> SoftFail = 0;
}

//=== Instruction Defs
{% for inst in instr_defs -%}
def {{ inst.varname }}: {{ namespace }}Inst<
  (outs {{ inst.outs }}), (ins {{ inst.ins }}),
  {{ inst.asmstr }},
  {{ inst.pattern }}>
{
{{ inst.params }}
{{ inst.bit_defs }}
{{ inst.bit_insts }}
{{ inst.attrs }}
}
{% endfor %}

//=== Pseudo Instruction Defs
def {{ namespace.lower() }}_ret_glue : SDNode<
  "{{ namespace }}ISD::RET_GLUE", SDTNone,
  [SDNPHasChain, SDNPOptInGlue, SDNPVariadic]>;

def PseudoRET: {{ namespace }}Inst<
  (outs), (ins),
  "",
  [({{ namespace.lower() }}_ret_glue)]>
{
  let isPseudo = 1;
  let isCodeGenOnly = 1;
  let isBarrier = 1;
  let isReturn = 1;
  let isTerminator = 1;
}


//== Gen Imm Pattern
// [TODO] auto generate from instruction semantics
def LO12S: SDNodeXForm<imm, [{
  return CurDAG->getTargetConstant(
    SignExtend64<12>(N->getZExtValue()),
    SDLoc(N),
    N->getValueType(0)
  );
}]>;
def HI20: SDNodeXForm<imm, [{
  return getImm(N, ((N->getZExtValue()+0x800) >> 12) & 0xfffff);
}]>;

def : Pat<(ImmS12:$in), (ADDI X0, ImmS12:$in)>;
def : Pat<(ImmHi20:$in), (LUI (HI20 imm:$in))>;
def : Pat<(Imm:$in), (ADDI (LUI (HI20 imm:$in)), (LO12S imm:$in))>;
