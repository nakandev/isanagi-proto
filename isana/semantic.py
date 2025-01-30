import ast
import inspect
from textwrap import dedent


op_table = {
    # BinOp
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
    # Compare
    # ast.Eq: "",
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
    if not isinstance(body_root[0].value, (ast.BinOp, ast.Compare)):
        return None
    if isinstance(body_root[0].value, ast.BinOp):
        op = body_root[0].value.op
        lhs_l = body_root[0].value.left
        lhs_r = body_root[0].value.right
    elif isinstance(body_root[0].value, ast.Compare):
        op = body_root[0].value.ops[0]
        lhs_l = body_root[0].value.left
        lhs_r = body_root[0].value.comparators[0]
    # -- check op
    if type(op) in op_table.keys():
        dag_op = op_table[type(op)]
    else:
        dag_op = None
        return None
    # print(dag_op or type(op))
    # -- check lhs_l
    if not isinstance(lhs_l, ast.Subscript):
        return None
    lhs_l_tp = lhs_l.value.attr
    lhs_l_name = lhs_l.slice.attr
    # -- check lhs_r
    if not isinstance(lhs_r, ast.Subscript):
        return None
    lhs_r_tp = lhs_r.value.attr
    lhs_r_name = lhs_r.slice.attr
    return (
        dag_op,
        (dst_name, dst_tp),
        (lhs_l_name, lhs_l_tp),
        (lhs_r_name, lhs_r_tp),
    )
