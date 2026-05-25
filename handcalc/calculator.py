from __future__ import annotations

from dataclasses import dataclass

from .evaluator import EvaluationError, evaluate_expression


_DIGITS = set("0123456789")
_OPERATORS = set("+-*/")
_BUTTON_VALUES = _DIGITS | _OPERATORS | {"C", "="}


@dataclass(frozen=True)
class CalculatorState:
    expression: str = ""
    error: str | None = None

    def apply(self, value: str) -> "CalculatorState":
        if value not in _BUTTON_VALUES:
            return self

        if value == "C":
            return CalculatorState()

        if value == "=":
            return self._evaluate()

        if self.error is not None:
            if value in _DIGITS:
                return CalculatorState(expression=value)
            return CalculatorState()

        if value in _OPERATORS:
            return self._append_operator(value)

        return CalculatorState(expression=self.expression + value)

    def _evaluate(self) -> "CalculatorState":
        try:
            return CalculatorState(expression=evaluate_expression(self.expression))
        except EvaluationError as exc:
            return CalculatorState(expression="Error", error=str(exc))

    def _append_operator(self, value: str) -> "CalculatorState":
        if not self.expression:
            if value == "-":
                return CalculatorState(expression="-")
            return self

        if self.expression[-1] in _OPERATORS:
            return CalculatorState(expression=self.expression[:-1] + value)

        return CalculatorState(expression=self.expression + value)
