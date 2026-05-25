import unittest

from handcalc.sizing import RenderSize, choose_render_size


class SizingTests(unittest.TestCase):
    def test_auto_size_fits_available_screen_and_preserves_camera_aspect(self):
        size = choose_render_size(camera_size=(640, 480), screen_size=(1920, 1080))

        self.assertLessEqual(size.width, int(1920 * 0.92))
        self.assertLessEqual(size.height, int(1080 * 0.82))
        self.assertAlmostEqual(size.width / size.height, 4 / 3, places=2)

    def test_auto_size_scales_down_for_small_screens(self):
        size = choose_render_size(camera_size=(640, 480), screen_size=(800, 600))

        self.assertLessEqual(size.width, int(800 * 0.92))
        self.assertLessEqual(size.height, int(600 * 0.82))
        self.assertAlmostEqual(size.width / size.height, 4 / 3, places=2)

    def test_auto_size_handles_very_small_screens(self):
        size = choose_render_size(camera_size=(640, 480), screen_size=(320, 240))

        self.assertLessEqual(size.width, 320)
        self.assertLessEqual(size.height, 240)
        self.assertGreaterEqual(size.width, 240)
        self.assertGreaterEqual(size.height, 180)

    def test_explicit_size_is_used_when_it_fits(self):
        size = choose_render_size(
            camera_size=(640, 480),
            screen_size=(1920, 1080),
            requested_size=(RenderSize(960, 720)),
        )

        self.assertEqual(size, RenderSize(960, 720))

    def test_partial_explicit_size_preserves_aspect(self):
        size = choose_render_size(
            camera_size=(1280, 720),
            screen_size=(1920, 1080),
            requested_size=RenderSize(1280, None),
        )

        self.assertEqual(size, RenderSize(1280, 720))


if __name__ == "__main__":
    unittest.main()
