import math
import unittest

from handcalc.evaluator import EvaluationError, evaluate_expression


class EvaluateExpressionTests(unittest.TestCase):
    def test_evaluates_basic_arithmetic_with_precedence(self):
        self.assertEqual(evaluate_expression("12+3*4-8/2"), "20")

    def test_formats_fractional_results_without_extra_zeroes(self):
        self.assertEqual(evaluate_expression("7/2"), "3.5")

    def test_rejects_unsafe_python_syntax(self):
        with self.assertRaises(EvaluationError):
            evaluate_expression("__import__('os').system('echo unsafe')")

    def test_rejects_division_by_zero(self):
        with self.assertRaises(EvaluationError):
            evaluate_expression("8/0")

    def test_rejects_non_finite_results(self):
        with self.assertRaises(EvaluationError):
            evaluate_expression(str(math.inf))


if __name__ == "__main__":
    unittest.main()
