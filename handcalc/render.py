from __future__ import annotations

from .buttons import Button, Point
from .calculator import CalculatorState
from .layout import CalculatorLayout


def draw_button(frame, cv2, button: Button, hover: bool = False, selected: bool = False) -> None:
    x, y = button.position
    fill = (22, 24, 28)
    border = (80, 90, 104)

    if hover:
        fill = (20, 135, 70)
        border = (40, 220, 120)
    if selected:
        fill = (0, 170, 215)
        border = (0, 235, 255)

    cv2.rectangle(frame, button.position, (x + button.width, y + button.height), fill, cv2.FILLED)
    cv2.rectangle(frame, button.position, (x + button.width, y + button.height), border, 3)

    font_scale, text_size = _fit_text(
        cv2,
        button.value,
        max_width=button.width - 18,
        max_height=button.height - 18,
        preferred_scale=min(1.85, max(0.95, button.width / 58)),
        thickness=2,
    )
    text_x = x + (button.width - text_size[0]) // 2
    text_y = y + (button.height + text_size[1]) // 2
    cv2.putText(frame, button.value, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2)


def draw_display(frame, cv2, state: CalculatorState, layout: CalculatorLayout) -> None:
    x, y = layout.display_top_left
    width, height = layout.display_size
    bottom_right = layout.display_bottom_right
    padding = max(10, height // 7)

    cv2.rectangle(frame, layout.display_top_left, bottom_right, (12, 14, 18), cv2.FILLED)
    cv2.rectangle(frame, layout.display_top_left, bottom_right, (75, 85, 100), 2)

    text = state.expression or "0"
    if len(text) > 18:
        text = text[-18:]

    font_scale, text_size = _fit_text(
        cv2,
        text,
        max_width=width - (2 * padding),
        max_height=height - (2 * padding),
        preferred_scale=min(2.0, max(1.0, height / 52)),
        thickness=2,
    )

    color = (0, 220, 255) if state.error is None else (40, 80, 255)
    text_x = x + padding
    text_y = y + (height + text_size[1]) // 2
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2)


def draw_status(frame, cv2, message: str, layout: CalculatorLayout) -> None:
    font_scale, _ = _fit_text(
        cv2,
        message,
        max_width=layout.frame_width - layout.status_position[0] - 20,
        max_height=28,
        preferred_scale=0.7,
        thickness=2,
    )
    cv2.putText(frame, message, layout.status_position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (210, 220, 230), 2)


def draw_pinch_feedback(frame, cv2, point: Point, distance: float, active: bool) -> None:
    color = (0, 240, 255) if active else (180, 180, 180)
    radius = 17 if active else 10
    cv2.circle(frame, point, radius, color, cv2.FILLED)
    cv2.putText(
        frame,
        f"pinch {distance:.0f}",
        (point[0] + 14, point[1] - 14),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        color,
        2,
    )


def _fit_text(cv2, text: str, max_width: int, max_height: int, preferred_scale: float, thickness: int):
    scale = preferred_scale
    while scale > 0.35:
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, thickness)
        if text_size[0] <= max_width and text_size[1] <= max_height:
            return scale, text_size
        scale -= 0.05

    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.35, thickness)
    return 0.35, text_size
