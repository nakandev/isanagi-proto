//=== Operands
{% for opcls in operand_clss -%}
def {{ opcls.varname }}: Operand<{{ opcls.basecls }}>;
{% endfor %}

//=== OperandTypes
{% for optp in operand_types -%}
def {{ optp.varname }} : IntImmLeaf<{{ optp.basecls }}, [{return Imm == (Imm & 0xff);}]>;
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
