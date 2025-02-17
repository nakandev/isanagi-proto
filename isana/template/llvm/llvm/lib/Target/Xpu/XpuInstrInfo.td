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

class BrImmS<int n, int s> : Operand<OtherVT> {
  let OperandType   = "OPERAND_PCREL";
  let EncoderMethod = "getImmOpValueRShift<" # s # ">";
  let DecoderMethod = "decodeSImmOperand<" # n # "," # s # ">";
}
{% for opcls in br_imm_operand_clss -%}
def {{ opcls.varname }}: BrImmS<{{ opcls.br_attr.width }},{{ opcls.br_attr.offset }}>;
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
def : Pat<(ImmS20O12:$in), (LUI (HI20 imm:$in))>;
def : Pat<(Imm:$in), (ADDI (LUI (HI20 imm:$in)), (LO12S imm:$in))>;


//== Set-ConditionCode Pattern

def : Pat<(seteq GPR:$rs1, GPR:$rs2), (SLTIU (XOR GPR:$rs1, GPR:$rs2), 1)>;
def : Pat<(setne GPR:$rs1, GPR:$rs2), (SLTU X0, (XOR GPR:$rs1, GPR:$rs2))>;
def : Pat<(setugt GPR:$rs1, GPR:$rs2), (SLTU GPR:$rs2, GPR:$rs1)>;
def : Pat<(setuge GPR:$rs1, GPR:$rs2), (XORI (SLTU GPR:$rs1, GPR:$rs2), 1)>;
def : Pat<(setule GPR:$rs1, GPR:$rs2), (XORI (SLTU GPR:$rs2, GPR:$rs1), 1)>;
def : Pat<(setgt GPR:$rs1, GPR:$rs2), (SLT GPR:$rs2, GPR:$rs1)>;
def : Pat<(setge GPR:$rs1, GPR:$rs2), (XORI (SLT GPR:$rs1, GPR:$rs2), 1)>;
def : Pat<(setle GPR:$rs1, GPR:$rs2), (XORI (SLT GPR:$rs2, GPR:$rs1), 1)>;

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

//== Branch/Jump Pattern
def PseudoBR: CustomXPUInst<
  (outs), (ins BrImmS20O1:$imm),
  "",
  [(br bb:$imm)]>,
  PseudoInstExpansion<(JAL X0, BrImmS20O1:$imm)>
{
  let isPseudo = 1;
  let isCodeGenOnly = 1;
  let isBarrier = 1;
  let isBranch = 1;
  let isTerminator = 1;
}

def : Pat<(brcond GPR:$cond, bb:$dst), (BNE GPR:$cond, X0, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setne  GPR:$lhs, 0)), bb:$dst), (BNE GPR:$lhs, X0, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (seteq  GPR:$lhs, 0)), bb:$dst), (BEQ GPR:$lhs, X0, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (seteq  GPR:$lhs, GPR:$rhs)), bb:$dst), (BEQ GPR:$lhs, GPR:$rhs, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setueq GPR:$lhs, GPR:$rhs)), bb:$dst), (BEQ GPR:$lhs, GPR:$rhs, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setne  GPR:$lhs, GPR:$rhs)), bb:$dst), (BNE GPR:$lhs, GPR:$rhs, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setune GPR:$lhs, GPR:$rhs)), bb:$dst), (BNE GPR:$lhs, GPR:$rhs, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setlt  GPR:$lhs, GPR:$rhs)), bb:$dst), (BNE (SLT  GPR:$lhs, GPR:$rhs), X0, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setult GPR:$lhs, GPR:$rhs)), bb:$dst), (BNE (SLTU GPR:$lhs, GPR:$rhs), X0, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setgt  GPR:$lhs, GPR:$rhs)), bb:$dst), (BNE (SLT  GPR:$rhs, GPR:$lhs), X0, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setugt GPR:$lhs, GPR:$rhs)), bb:$dst), (BNE (SLTU GPR:$rhs, GPR:$lhs), X0, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setle  GPR:$lhs, GPR:$rhs)), bb:$dst), (BEQ (SLT  GPR:$rhs, GPR:$lhs), X0, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setule GPR:$lhs, GPR:$rhs)), bb:$dst), (BEQ (SLTU GPR:$rhs, GPR:$lhs), X0, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setge  GPR:$lhs, GPR:$rhs)), bb:$dst), (BEQ (SLT  GPR:$lhs, GPR:$rhs), X0, BrImmS12O1:$dst)>;
def : Pat<(brcond (i32 (setuge GPR:$lhs, GPR:$rhs)), bb:$dst), (BEQ (SLTU GPR:$lhs, GPR:$rhs), X0, BrImmS12O1:$dst)>;

def PseudoBRIND: CustomXPUInst<
  (outs), (ins GPR:$rs1, ImmS12:$imm),
  "",
  []>,
  PseudoInstExpansion<(JALR X0, GPR:$rs1, ImmS12:$imm)>
{
  let isPseudo = 1;
  let isCodeGenOnly = 1;
  let isBarrier = 1;
  let isBranch = 1;
  let isIndirectBranch = 1;
  let isTerminator = 1;
}
def : Pat<(brind GPR:$rs1), (PseudoBRIND GPR:$rs1, 0)>;
def : Pat<(brind (add GPR:$rs1, ImmS12:$imm)), (PseudoBRIND GPR:$rs1, ImmS12:$imm)>;

def SDT_CustomXPUSelectCC : SDTypeProfile<1, 5, [SDTCisSameAs<1, 2>,
                                                 SDTCisSameAs<0, 4>,
                                                 SDTCisSameAs<4, 5>]>;
def SelectCC : SDNode<"CustomXPUISD::SELECT_CC", SDT_CustomXPUSelectCC, [SDNPInGlue]>;
def Select_GPR : CustomXPUInst<
  (outs GPR:$dst), (ins GPR:$lhs, GPR:$rhs, ImmS12:$imm, GPR:$truev, GPR:$falsev),
  "",
  [(set GPR:$dst, (SelectCC GPR:$lhs, GPR:$rhs, (i32 imm:$imm), GPR:$truev, GPR:$falsev))]>
{
  let isPseudo = 1;
  let isCodeGenOnly = 1;
  let usesCustomInserter = 1;
}
def : Pat<(SelectCC GPR:$lhs, 0, (i32 imm:$imm), GPR:$truev, GPR:$falsev),
          (Select_GPR GPR:$lhs, X0, imm:$imm, GPR:$truev, GPR:$falsev)>;
