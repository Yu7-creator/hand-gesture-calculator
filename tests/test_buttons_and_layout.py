import unittest

from handcalc.buttons import Button
from handcalc.layout import build_calculator_buttons, build_calculator_layout


class ButtonTests(unittest.TestCase):
    def test_contains_point_includes_edges_inside_button(self):
        button = Button(position=(10, 20), width=80, height=80, value="7")

        self.assertTrue(button.contains_point(10, 20))
        self.assertTrue(button.contains_point(90, 100))
        self.assertFalse(button.contains_point(91, 100))
        self.assertFalse(button.contains_point(90, 101))

    def test_build_calculator_buttons_creates_expected_grid(self):
        buttons = build_calculator_buttons(origin=(50, 150), button_size=80, gap=20)

        self.assertEqual(len(buttons), 16)
        self.assertEqual([button.value for button in buttons[:4]], ["7", "8", "9", "+"])
        self.assertEqual(buttons[0].position, (50, 150))
        self.assertEqual(buttons[-1].value, "/")
        self.assertEqual(buttons[-1].position, (350, 450))

    def test_responsive_layout_fits_inside_480p_frame(self):
        layout = build_calculator_layout(frame_width=640, frame_height=480)

        self.assertEqual(layout.frame_width, 640)
        self.assertEqual(layout.frame_height, 480)
        self.assertGreaterEqual(layout.display_top_left[0], 0)
        self.assertGreaterEqual(layout.display_top_left[1], 0)
        self.assertLessEqual(layout.display_bottom_right[0], 640)
        self.assertLessEqual(layout.display_bottom_right[1], 480)
        self.assertLessEqual(layout.status_position[1], 470)

        for button in layout.buttons:
            x, y = button.position
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x + button.width, 640)
            self.assertLessEqual(y + button.height, 480)

    def test_responsive_layout_uses_larger_demo_canvas(self):
        layout = build_calculator_layout(frame_width=960, frame_height=720)

        self.assertEqual(layout.frame_width, 960)
        self.assertEqual(layout.frame_height, 720)
        self.assertGreater(layout.buttons[0].width, 90)
        self.assertLessEqual(layout.buttons[-1].position[1] + layout.buttons[-1].height, 720)

    def test_responsive_layout_centers_calculator_horizontally(self):
        layout = build_calculator_layout(frame_width=1280, frame_height=720)
        left = layout.display_top_left[0]
        right = layout.display_bottom_right[0]

        self.assertLessEqual(abs(left - (1280 - right)), 1)
        for button in layout.buttons:
            self.assertGreaterEqual(button.position[0], left)
            self.assertLessEqual(button.position[0] + button.width, right)

    def test_responsive_layout_fits_inside_compact_window(self):
        layout = build_calculator_layout(frame_width=300, frame_height=220)

        self.assertLessEqual(layout.display_bottom_right[0], 300)
        self.assertLessEqual(layout.display_bottom_right[1], 220)
        self.assertLessEqual(layout.status_position[1], 220)

        for button in layout.buttons:
            x, y = button.position
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x + button.width, 300)
            self.assertLessEqual(y + button.height, 220)


if __name__ == "__main__":
    unittest.main()
