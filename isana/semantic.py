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


def estimate_load_immediate_ops(instructions):
    pass
