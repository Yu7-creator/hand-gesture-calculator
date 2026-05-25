from __future__ import annotations

from dataclasses import dataclass

from .buttons import Button, Point


KEYS = (
    ("7", "8", "9", "+"),
    ("4", "5", "6", "-"),
    ("1", "2", "3", "*"),
    ("C", "0", "=", "/"),
)


@dataclass(frozen=True)
class CalculatorLayout:
    frame_width: int
    frame_height: int
    buttons: list[Button]
    display_top_left: Point
    display_size: tuple[int, int]
    status_position: Point

    @property
    def display_bottom_right(self) -> Point:
        x, y = self.display_top_left
        width, height = self.display_size
        return (x + width, y + height)


def build_calculator_buttons(
    origin: Point = (50, 150),
    button_size: int = 80,
    gap: int = 20,
) -> list[Button]:
    buttons: list[Button] = []
    start_x, start_y = origin
    stride = button_size + gap

    for row_index, row in enumerate(KEYS):
        for column_index, value in enumerate(row):
            position = (
                start_x + column_index * stride,
                start_y + row_index * stride,
            )
            buttons.append(Button(position=position, width=button_size, height=button_size, value=value))

    return buttons


def build_calculator_layout(frame_width: int = 960, frame_height: int = 720) -> CalculatorLayout:
    if frame_width < 240 or frame_height < 200:
        raise ValueError("Frame must be at least 240x200 for the calculator layout.")

    side_margin = max(6, min(56, frame_width // 16))
    top_margin = max(6, min(48, frame_height // 16))
    gap = max(4, min(20, frame_height // 40))
    display_height = max(28, min(90, frame_height // 8))
    status_reserve = max(16, min(44, frame_height // 14))
    bottom_margin = max(6, min(28, frame_height // 24))

    grid_top = top_margin + display_height + gap
    available_grid_height = frame_height - grid_top - status_reserve - bottom_margin
    available_panel_width = min(frame_width - (2 * side_margin), int(frame_width * 0.54))

    button_from_height = (available_grid_height - (3 * gap)) // 4
    button_from_width = (available_panel_width - (3 * gap)) // 4
    button_size = min(118, button_from_height, button_from_width)
    if button_size < 18:
        raise ValueError("Frame is too small for the calculator layout.")

    grid_width = (4 * button_size) + (3 * gap)
    panel_left = max(0, (frame_width - grid_width) // 2)
    buttons = build_calculator_buttons(
        origin=(panel_left, grid_top),
        button_size=button_size,
        gap=gap,
    )
    grid_bottom = grid_top + (4 * button_size) + (3 * gap)
    status_y = min(frame_height - bottom_margin, grid_bottom + (status_reserve // 2))

    return CalculatorLayout(
        frame_width=frame_width,
        frame_height=frame_height,
        buttons=buttons,
        display_top_left=(panel_left, top_margin),
        display_size=(grid_width, display_height),
        status_position=(panel_left, status_y),
    )
