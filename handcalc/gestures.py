from __future__ import annotations

import math
from dataclasses import dataclass

from .buttons import Point


THUMB_TIP = 4
INDEX_TIP = 8


@dataclass(frozen=True)
class PinchEvent:
    clicked: bool
    point: Point
    distance: float


class PinchClickDetector:
    def __init__(self, threshold: float = 40.0, click_delay: float = 0.75) -> None:
        self.threshold = threshold
        self.click_delay = click_delay
        self._last_click_time = float("-inf")

    def detect(self, landmarks: list[Point], now: float) -> PinchEvent:
        distance = pinch_distance(landmarks)
        point = pinch_midpoint(landmarks)
        can_click = distance < self.threshold and (now - self._last_click_time) >= self.click_delay

        if can_click:
            self._last_click_time = now

        return PinchEvent(clicked=can_click, point=point, distance=distance)


def pinch_distance(landmarks: list[Point]) -> float:
    thumb = landmarks[THUMB_TIP]
    index = landmarks[INDEX_TIP]
    return math.hypot(index[0] - thumb[0], index[1] - thumb[1])


def pinch_midpoint(landmarks: list[Point]) -> Point:
    thumb = landmarks[THUMB_TIP]
    index = landmarks[INDEX_TIP]
    return ((thumb[0] + index[0]) // 2, (thumb[1] + index[1]) // 2)
