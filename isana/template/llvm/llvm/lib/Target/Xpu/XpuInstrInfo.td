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


//== Generate Immediate Pattern
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


//== Load/Store Pattern
class AlignedLoad<PatFrag Node>: PatFrag<(ops node:$ptr), (Node node:$ptr), [{
  LoadSDNode *LD = cast<LoadSDNode>(N);
  return LD->getMemoryVT().getSizeInBits()/8 <= LD->getAlignment();
}]>;
class AlignedStore<PatFrag Node>: PatFrag<(ops node:$val, node:$ptr), (Node node:$val, node:$ptr), [{
  StoreSDNode *SD = cast<StoreSDNode>(N);
  return SD->getMemoryVT().getSizeInBits()/8 <= SD->getAlignment();
}]>;

def load_a         : AlignedLoad<load       >;
def sextloadi8_a   : AlignedLoad<sextloadi8 >;
def zextloadi8_a   : AlignedLoad<zextloadi8 >;
def sextloadi16_a  : AlignedLoad<sextloadi16>;
def zextloadi16_a  : AlignedLoad<zextloadi16>;
def  extloadi16_a  : AlignedLoad< extloadi16>;
def sextloadi32_a  : AlignedLoad<sextloadi32>;
def zextloadi32_a  : AlignedLoad<zextloadi32>;
def  extloadi32_a  : AlignedLoad< extloadi32>;
def store_a         : AlignedStore<store        >;
def truncstorei8_a  : AlignedStore<truncstorei8 >;
def truncstorei16_a : AlignedStore<truncstorei16>;
def truncstorei32_a : AlignedStore<truncstorei32>;

def FIAddr : ComplexPattern<iPTR, 2, "SelectAddrFrameIndexRegImm", [frameindex, add], []>;
def : Pat<(FIAddr (iPTR GPR:$rs1), Imm:$imm),
          (ADD GPR:$rs1, (ADDI (LUI (HI20 imm:$imm)), (LO12S imm:$imm)))>;

def AddrReg      : ComplexPattern<iPTR, 2, "SelectAddrRegImm", [], []>;

class LoadPattern<PatFrag LoadOp, {{ namespace }}Inst Inst> :
  Pat<(LoadOp (AddrReg GPR:$rs1, Imm:$imm)),
      (Inst (ADD GPR:$rs1, (ADDI (LUI (HI20 imm:$imm)), (LO12S imm:$imm))), 0)>;
class StorePattern<PatFrag StoreOp, {{ namespace }}Inst Inst, RegisterClass RC> :
  Pat<(StoreOp RC:$rs2, (AddrReg GPR:$rs1, Imm:$imm)),
      (Inst RC:$rs2, (ADD GPR:$rs1, (ADDI (LUI (HI20 imm:$imm)), (LO12S imm:$imm))), 0)>;

def : LoadPattern<sextloadi8 , LB>;
def : LoadPattern< extloadi8 , LB>;
def : LoadPattern<sextloadi16, LH>;
def : LoadPattern< extloadi16, LH>;
def : LoadPattern<load       , LW>;
def : LoadPattern<zextloadi8 , LBU>;
def : LoadPattern<zextloadi16, LHU>;
def : StorePattern<truncstorei8 , SB, GPR>;
def : StorePattern<truncstorei16, SH, GPR>;
def : StorePattern<store        , SW, GPR>;
