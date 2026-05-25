import unittest

from handcalc.cli import build_parser


class CliTests(unittest.TestCase):
    def test_parser_exposes_runtime_options(self):
        parser = build_parser()

        args = parser.parse_args(
            [
                "--camera-index",
                "2",
                "--click-delay",
                "0.25",
                "--pinch-threshold",
                "32",
                "--model-path",
                "models/custom.task",
                "--frame-width",
                "960",
                "--frame-height",
                "720",
            ]
        )

        self.assertEqual(args.camera_index, 2)
        self.assertEqual(args.click_delay, 0.25)
        self.assertEqual(args.pinch_threshold, 32.0)
        self.assertEqual(args.model_path, "models/custom.task")
        self.assertEqual(args.frame_width, 960)
        self.assertEqual(args.frame_height, 720)


if __name__ == "__main__":
    unittest.main()
