"""A safe arithmetic evaluator (restricted AST).

RLVR math verification often needs to compare a predicted answer against a gold
answer that is itself an expression ("1/2 + 1/3"). We evaluate such strings with
an allow-listed AST walker — no ``eval``, no names, no calls — so untrusted model
output can never execute code. Results are exact ``Fraction``s where possible.
"""
from __future__ import annotations

import ast
from fractions import Fraction

_BIN_OPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a ** b,
    ast.Mod: lambda a, b: a % b,
}
_UNARY_OPS = {
    ast.UAdd: lambda a: a,
    ast.USub: lambda a: -a,
}


class ExprError(ValueError):
    pass


def _eval(node: ast.AST) -> Fraction:
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ExprError(f"unsupported constant: {node.value!r}")
        return Fraction(node.value).limit_denominator(10 ** 9)
    if isinstance(node, ast.BinOp):
        op = _BIN_OPS.get(type(node.op))
        if op is None:
            raise ExprError(f"unsupported operator: {type(node.op).__name__}")
        if isinstance(node.op, ast.Pow):
            base, exp = _eval(node.left), _eval(node.right)
            if exp.denominator != 1:
                raise ExprError("fractional exponents are not supported")
            return base ** int(exp)
        return op(_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        op = _UNARY_OPS.get(type(node.op))
        if op is None:
            raise ExprError(f"unsupported unary operator: {type(node.op).__name__}")
        return op(_eval(node.operand))
    raise ExprError(f"unsupported syntax: {type(node).__name__}")


def safe_eval(expr: str) -> Fraction:
    """Evaluate a pure-arithmetic expression to an exact Fraction."""
    expr = expr.strip()
    if not expr:
        raise ExprError("empty expression")
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:  # noqa: PERF203
        raise ExprError(f"could not parse {expr!r}") from exc
    return _eval(tree)
