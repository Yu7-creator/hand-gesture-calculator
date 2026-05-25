import unittest

from handcalc.calculator import CalculatorState


class CalculatorStateTests(unittest.TestCase):
    def test_appends_digits_and_operators(self):
        state = CalculatorState()

        for value in ["1", "2", "+", "3"]:
            state = state.apply(value)

        self.assertEqual(state.expression, "12+3")
        self.assertIsNone(state.error)

    def test_clear_resets_expression_and_error(self):
        state = CalculatorState(expression="Error", error="invalid")

        state = state.apply("C")

        self.assertEqual(state.expression, "")
        self.assertIsNone(state.error)

    def test_equals_replaces_expression_with_result(self):
        state = CalculatorState(expression="6*7")

        state = state.apply("=")

        self.assertEqual(state.expression, "42")
        self.assertIsNone(state.error)

    def test_invalid_equals_shows_error_and_next_digit_starts_fresh(self):
        state = CalculatorState(expression="7/0").apply("=")

        self.assertEqual(state.expression, "Error")
        self.assertIsNotNone(state.error)

        state = state.apply("5")

        self.assertEqual(state.expression, "5")
        self.assertIsNone(state.error)

    def test_ignores_unknown_button_values(self):
        state = CalculatorState(expression="9")

        self.assertEqual(state.apply("x"), state)


if __name__ == "__main__":
    unittest.main()
