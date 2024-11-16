import ast
import inspect
from textwrap import dedent


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
