import unittest

from handcalc.gestures import PinchClickDetector, pinch_distance, pinch_midpoint


class GestureTests(unittest.TestCase):
    def test_pinch_distance_and_midpoint_use_thumb_and_index_tips(self):
        landmarks = [(0, 0)] * 21
        landmarks[4] = (10, 10)
        landmarks[8] = (40, 50)

        self.assertEqual(pinch_distance(landmarks), 50.0)
        self.assertEqual(pinch_midpoint(landmarks), (25, 30))

    def test_detector_clicks_once_then_respects_cooldown(self):
        detector = PinchClickDetector(threshold=40, click_delay=1.0)
        landmarks = [(0, 0)] * 21
        landmarks[4] = (10, 10)
        landmarks[8] = (20, 20)

        first = detector.detect(landmarks, now=10.0)
        second = detector.detect(landmarks, now=10.5)
        third = detector.detect(landmarks, now=11.1)

        self.assertTrue(first.clicked)
        self.assertFalse(second.clicked)
        self.assertTrue(third.clicked)
        self.assertEqual(first.point, (15, 15))

    def test_detector_does_not_click_when_pinch_is_too_wide(self):
        detector = PinchClickDetector(threshold=10, click_delay=0.5)
        landmarks = [(0, 0)] * 21
        landmarks[4] = (0, 0)
        landmarks[8] = (30, 40)

        event = detector.detect(landmarks, now=1.0)

        self.assertFalse(event.clicked)
        self.assertEqual(event.point, (15, 20))


if __name__ == "__main__":
    unittest.main()
