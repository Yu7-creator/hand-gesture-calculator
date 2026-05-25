from __future__ import annotations

from dataclasses import dataclass


Point = tuple[int, int]


@dataclass(frozen=True)
class Button:
    position: Point
    width: int
    height: int
    value: str

    def contains_point(self, x: int, y: int) -> bool:
        left, top = self.position
        right = left + self.width
        bottom = top + self.height
        return left <= x <= right and top <= y <= bottom
