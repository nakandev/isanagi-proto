import ast
import inspect
from textwrap import dedent


op_alu_table = {
    ast.Add: "add",
    ast.Sub: "sub",
    ast.Mult: "mul",
    ast.FloorDiv: "sdiv",
    ast.Mod: "srem",
    ast.LShift: "shl",
    ast.RShift: "sra",
    ast.BitAnd: "and",
    ast.BitOr: "or",
    ast.BitXor: "xor",
}


op_aluu_table = {
    ast.FloorDiv: "udiv",
    ast.Mod: "urem",
    ast.RShift: "srl",
}

op_cmp_table = {
    ast.Eq: "seteq",
    ast.NotEq: "setne",
    ast.Gt: "setgt",
    ast.Lt: "setlt",
    ast.GtE: "setge",
    ast.LtE: "setle",
}

op_cmpu_table = {
    ast.Gt: "setugt",
    ast.Lt: "setult",
    ast.GtE: "setuge",
    ast.LtE: "setule",
}


def _is_pc_in_lhs(node):
    # check "ctx.PCR.pc" in lhs
    if not isinstance(node.targets, list):
        return False
    if not (isinstance(node.targets[0], ast.Attribute) and node.targets[0].attr == "pc"):
        return False
    if not (isinstance(node.targets[0].value, ast.Attribute) and node.targets[0].value.attr == "PCR"):
        return False
    return True


def _is_pc_in_rhs(node):
    # check no "ctx.PCR.pc + X" or "X + ctx.PCR.pc" in rhs
    # print(ast.dump(node, indent=4))
    if not isinstance(node.value, ast.BinOp):
        return False
    left = node.value.left
    if isinstance(left, ast.Attribute) and left.attr == "pc":
        if isinstance(left.value, ast.Attribute) and left.value.attr == "PCR":
            return True
    right = node.value.right
    if isinstance(right, ast.Attribute) and right.attr == "pc":
        if isinstance(right.value, ast.Attribute) and right.value.attr == "PCR":
            return True
    return False


def may_change_pc_absolute(semantic):
    code = inspect.getsource(semantic)
    code = dedent(code)
    for node in ast.walk(ast.parse(code)):
        if not isinstance(node, ast.Assign):
            continue
        if _is_pc_in_lhs(node) and not _is_pc_in_rhs(node):
            return True
    return False


def may_change_pc_relative(semantic):
    code = inspect.getsource(semantic)
    code = dedent(code)
    # check if 'ctx.PCR.pc = ctx.PCR.pc + X' exists
    for node in ast.walk(ast.parse(code)):
        if not isinstance(node, ast.Assign):
            continue
        if _is_pc_in_lhs(node) and _is_pc_in_rhs(node):
            return True
    # check if 'ctx.PCR.pc += ' exists
    for node in ast.walk(ast.parse(code)):
        if not isinstance(node, ast.AugAssign):
            continue
        if not (isinstance(node.target, ast.Attribute) and node.target.attr == "pc"):
            continue
        if not (isinstance(node.target.value, ast.Attribute) and node.target.value.attr == "PCR"):
            continue
        break
    else:
        return False
    return True


def may_take_memory_address(semantic):
    code = inspect.getsource(semantic)
    code = dedent(code)
    for node in ast.walk(ast.parse(code)):
        if not (isinstance(node, ast.Attribute) and node.attr in ("read", "write")):
            continue
        if not (isinstance(node.value, ast.Attribute) and node.value.attr == "Mem"):
            continue
        break
    else:
        return False
    return True


def get_alu_dag(semantic):
    alu_category = "alu"
    code = inspect.getsource(semantic)
    code = dedent(code)
    # print(ast.dump(ast.parse(code), indent=4))
    # check if only one expression exists
    root = ast.parse(code)
    body_root = root.body[0].body
    if not (len(body_root) == 1 and isinstance(body_root[0], ast.Assign)):
        return None
    # check if lhs 'Reg[reg_no]'
    dsts = body_root[0].targets
    if not (len(dsts) == 1 and isinstance(dsts[0], ast.Subscript)):
        return None
    dst_tp = dsts[0].value.attr
    dst_name = dsts[0].slice.attr
    # check if rhs 'Reg[reg_no] op Reg[reg_no]'
    if isinstance(body_root[0].value, ast.BinOp):
        alu_category = "alu"
        op_check_table = op_alu_table
        op = body_root[0].value.op
        rhs_l = body_root[0].value.left
        rhs_r = body_root[0].value.right
    elif isinstance(body_root[0].value, ast.Compare):
        alu_category = "cmp"
        op_check_table = op_cmp_table
        op = body_root[0].value.ops[0]
        rhs_l = body_root[0].value.left
        rhs_r = body_root[0].value.comparators[0]
    else:
        return None
    # -- check unsigned
    unsigned_l, unsigned_r = False, False
    if isinstance(rhs_l, ast.Call):
        f_name = rhs_l.func.id
        # f_arg0 = rhs_l.args[0].id
        f_arg1 = rhs_l.args[1]
        if f_name != "unsigned":
            return None
        unsigned_l = True
        rhs_l = f_arg1
    if isinstance(rhs_r, ast.Call):
        f_name = rhs_r.func.id
        # f_arg0 = rhs_r.args[0].id
        f_arg1 = rhs_r.args[1]
        if f_name != "unsigned":
            return None
        unsigned_r = True
        rhs_r = f_arg1
    if unsigned_l or unsigned_r:
        if alu_category == "alu":
            op_check_table = op_aluu_table
        elif alu_category == "cmp":
            op_check_table = op_cmpu_table
    # -- check op
    if type(op) in op_check_table.keys():
        dag_op = op_check_table[type(op)]
    else:
        return None
    # print("#dag_op", dag_op or type(op))
    # -- check rhs_l
    if isinstance(rhs_l, ast.Subscript):
        rhs_l_tp = rhs_l.value.attr
        rhs_l_name = rhs_l.slice.attr
    else:
        return None
    # -- check rhs_r
    if isinstance(rhs_r, ast.Subscript):
        rhs_r_tp = rhs_r.value.attr
        rhs_r_name = rhs_r.slice.attr
    elif isinstance(rhs_r, ast.Attribute):
        rhs_r_tp = "UnknownImm"
        rhs_r_name = rhs_r.attr
    else:
        return None
    return (
        dag_op,
        (dst_name, dst_tp),
        (rhs_l_name, rhs_l_tp, unsigned_l),
        (rhs_r_name, rhs_r_tp, unsigned_r),
    )


def may_load_immediate(semantic):
    code = inspect.getsource(semantic)
    code = dedent(code)
    # print(ast.dump(ast.parse(code), indent=4))
    # check if 'ctx.GPR = ins.Imm
    root = ast.parse(code)
    body_root = root.body[0].body
    if not (len(body_root) == 1 and isinstance(body_root[0], ast.Assign)):
        return None
    # check if lhs 'GPR[reg_no]'
    dsts = body_root[0].targets
    if not (len(dsts) == 1 and isinstance(dsts[0], ast.Subscript)):
        return None
    dst_tp = dsts[0].value.attr
    # dst_name = dsts[0].slice.attr
    if dst_tp != "GPR":
        return None
    # check if rhs 'ins.imm'
    src = body_root[0].value
    if not isinstance(src, ast.Attribute):
        return None
    src_tp = src.value.id
    src_name = src.attr
    if not (src_tp == "ins" and src_name == "imm"):
        return None
    return True


def estimate_load_immediate_ops(isa):
    li32 = None
    li_s = []
    lui_s = []
    addi_s = []
    for cls in isa.instructions:
        instr = cls()
        instr.isa = isa
        instr.decode(instr.opc)  # dummy decode as all parameter is 0
        if may_load_immediate(instr.semantic):
            r_tp = instr.params.inputs["imm"].type_
            imm = next(filter(lambda im: im.label == r_tp, isa.immediates), None)
            if imm.offset == 0:
                li_s.append((instr, imm))
                if imm.width == 32:
                    li32 = (instr, imm)
            else:
                lui_s.append((instr, imm))
            continue
        dag = get_alu_dag(instr.semantic)
        if dag:
            (op, (dst_name, dst_tp), (l_name, l_tp, l_u), (r_name, r_tp, r_u)) = dag
            if op == "add" and r_name == "imm":
                r_tp = instr.params.inputs[r_name].type_
                imm = next(filter(lambda im: im.label == r_tp, isa.immediates), None)
                addi_s.append((instr, imm))
    lui_addi_s = []
    for (lui, lui_imm) in lui_s:
        for (addi, addi_imm) in addi_s:
            if lui_imm.offset == addi_imm.width:
                lui_addi_s.append(((lui, lui_imm), (addi, addi_imm)))
                if lui_imm.width + lui_imm.offset == 32 and not li32:
                    li32 = ((lui, lui_imm), (addi, addi_imm))
    return (li32, tuple(li_s), tuple(lui_s), tuple(addi_s), tuple(lui_addi_s))


def _gen_sdnodexform(imm, signed_lower=False):
    if signed_lower:
        half = hex(2 ** (imm.offset - 1)) if imm.offset > 0 else 0
        vstr = f"(N->getZExtValue()+{half})>>{imm.offset}"
        X = "XX"
    else:
        vstr = f"N->getZExtValue()>>{imm.offset}"
        X = "X"
    if hasattr(imm, "signed"):
        vstr = f"SignExtend64<{imm.width}>({vstr})"
    else:
        mask = hex(2 ** imm.width - 1)
        vstr = f"(({vstr}) & {mask})"
    s = "\n".join([
        f"def {imm.label}{X}: SDNodeXForm<imm, [{{",
        "  return CurDAG->getTargetConstant(",
        f"    {vstr},SDLoc(N),N->getValueType(0)",
        "  );",
        "}]>;"
    ])
    return s


def estimate_load_immediate_dag(isa):
    li_ops = estimate_load_immediate_ops(isa)
    (li32, li_s, lui_s, addi_s, lui_addi_s) = li_ops
    zeroreg = None
    for group in isa.registers:
        for reg in group.regs:
            if reg.is_zero:
                zeroreg = reg
                break
    immxs = []
    dags = []
    imm32 = None
    for imm in isa.immediates:
        if imm.width == 32 and imm.offset == 0:
            imm32 = imm
            break
    for ops in (li32,) + li_s + lui_s + addi_s:
        if isinstance(ops[0], tuple):
            # lui
            op, lui_imm = ops[0]
            immtp = lui_imm.label
            lui_str = [op.opn.upper()]
            for param in op.params.inputs.values():
                if param.type_ == immtp:
                    lui_str.append(f"({immtp}XX imm:$imm)")
                else:
                    if zeroreg:
                        lui_str.append(zeroreg.label.upper())
                    else:
                        raise Exception("cannot generate load immediate dag")
            lui_str = " ".join(lui_str)
            # addi
            op, addi_imm = ops[1]
            immtp = addi_imm.label
            opstr = []
            for param in op.params.inputs.values():
                if param.type_ == immtp:
                    opstr.append(f"({immtp}X imm:$imm)")
                else:
                    opstr.append(f"({lui_str})")
            opstr = op.opn.upper() + " " + ", ".join(opstr)
            if ops == li32:
                if imm32:
                    dags.append((imm32.label, opstr))
                else:
                    dags.append(("i32imm", opstr))
            else:
                dags.append((immtp, opstr))
            immx = (lui_imm, hasattr(addi_imm, "signed"))
            if immx not in immxs:
                immxs.append(immx)
            immx = (addi_imm, False)
            if immx not in immxs:
                immxs.append(immx)
        else:
            op, imm = ops
            r_tp = op.params.inputs["imm"].type_
            imm = next(filter(lambda im: im.label == r_tp, isa.immediates), None)
            immtp = imm.label
            opstr = []
            for param in op.params.inputs.values():
                if param.type_ == immtp:
                    opstr.append(f"({immtp}X imm:$imm)")
                else:
                    if zeroreg:
                        opstr.append(zeroreg.label.upper())
                    else:
                        raise Exception("cannot generate load immediate dag")
            opstr = op.opn.upper() + " " + ", ".join(opstr)
            dags.append((immtp, opstr))
            immx = (imm, False)
            if immx not in immxs:
                immxs.append(immx)
    xforms = []
    for immx in immxs:
        imm, signed = immx
        xforms.append(_gen_sdnodexform(imm, signed))
    return xforms, dags
