from __future__ import annotations

import ast
import math
import operator
from collections.abc import Callable


class EvaluationError(ValueError):
    """Raised when a calculator expression cannot be evaluated safely."""


_BINARY_OPERATORS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def evaluate_expression(expression: str) -> str:
    """Evaluate a small arithmetic expression and return a display string."""

    normalized = expression.strip()
    if not normalized:
        raise EvaluationError("Enter an expression first.")
    if len(normalized) > 80:
        raise EvaluationError("Expression is too long.")

    try:
        tree = ast.parse(normalized, mode="eval")
        result = _evaluate_node(tree)
    except EvaluationError:
        raise
    except (SyntaxError, RecursionError, ZeroDivisionError, OverflowError) as exc:
        raise EvaluationError("Invalid arithmetic expression.") from exc

    if not math.isfinite(result):
        raise EvaluationError("Result is not finite.")

    return _format_result(result)


def _evaluate_node(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _evaluate_node(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise EvaluationError("Only numeric values are allowed.")
        value = float(node.value)
        if not math.isfinite(value):
            raise EvaluationError("Only finite numbers are allowed.")
        return value

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)
        operation = _BINARY_OPERATORS.get(operator_type)
        if operation is None:
            raise EvaluationError("Only +, -, *, and / are allowed.")
        return operation(_evaluate_node(node.left), _evaluate_node(node.right))

    if isinstance(node, ast.UnaryOp):
        operator_type = type(node.op)
        operation = _UNARY_OPERATORS.get(operator_type)
        if operation is None:
            raise EvaluationError("Only unary + and - are allowed.")
        return operation(_evaluate_node(node.operand))

    raise EvaluationError("Unsupported expression.")


def _format_result(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return format(value, ".10g")
