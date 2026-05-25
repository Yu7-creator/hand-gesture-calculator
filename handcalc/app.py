from __future__ import annotations

import time
from dataclasses import dataclass

from .calculator import CalculatorState
from .gestures import PinchClickDetector
from .layout import build_calculator_layout
from .render import draw_button, draw_display, draw_pinch_feedback, draw_status
from .sizing import RenderSize, choose_render_size, detect_screen_size
from .vision import HandTracker


@dataclass(frozen=True)
class AppConfig:
    camera_index: int = 0
    click_delay: float = 0.75
    pinch_threshold: float = 40.0
    model_path: str | None = None
    frame_width: int | None = None
    frame_height: int | None = None
    window_title: str = "HandCalc Gesture Calculator"


def run(config: AppConfig) -> int:
    import cv2

    capture = cv2.VideoCapture(config.camera_index)
    if not capture.isOpened():
        print(f"Could not open camera index {config.camera_index}.")
        return 1

    if config.frame_width is not None:
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.frame_width)
    if config.frame_height is not None:
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.frame_height)

    camera_size = _camera_size(capture)
    render_size = choose_render_size(
        camera_size=camera_size,
        screen_size=detect_screen_size(),
        requested_size=RenderSize(config.frame_width, config.frame_height),
    )
    layout = build_calculator_layout(render_size.width, render_size.height)
    buttons = layout.buttons
    state = CalculatorState()
    detector = PinchClickDetector(threshold=config.pinch_threshold, click_delay=config.click_delay)
    selected_value: str | None = None
    selected_until = 0.0

    try:
        cv2.namedWindow(config.window_title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(config.window_title, render_size.width, render_size.height)
        with HandTracker(model_path=config.model_path) as tracker:
            while True:
                success, frame = capture.read()
                if not success:
                    print("Could not read a frame from the camera.")
                    return 1

                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (render_size.width, render_size.height), interpolation=cv2.INTER_AREA)
                now = time.time()
                hovered_value = None
                landmarks, hand_landmarks = tracker.detect(frame, cv2)

                if landmarks is not None and hand_landmarks is not None:
                    tracker.draw(frame, hand_landmarks)
                    event = detector.detect(landmarks, now)
                    hovered_value = _button_at_point(buttons, event.point)

                    if event.clicked and hovered_value is not None:
                        state = state.apply(hovered_value)
                        selected_value = hovered_value
                        selected_until = now + 0.2

                    draw_pinch_feedback(frame, cv2, event.point, event.distance, event.clicked)

                draw_display(frame, cv2, state, layout)
                for button in buttons:
                    draw_button(
                        frame,
                        cv2,
                        button,
                        hover=button.value == hovered_value,
                        selected=button.value == selected_value and now < selected_until,
                    )

                draw_status(
                    frame,
                    cv2,
                    "Pinch thumb + index to click. Press q to quit.",
                    layout,
                )

                cv2.imshow(config.window_title, frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    return 0

                window_size = _window_image_size(cv2, config.window_title)
                if _should_relayout(render_size, window_size):
                    render_size = window_size
                    layout = build_calculator_layout(render_size.width, render_size.height)
                    buttons = layout.buttons
    finally:
        capture.release()
        cv2.destroyAllWindows()


def _button_at_point(buttons, point: tuple[int, int]) -> str | None:
    x, y = point
    for button in buttons:
        if button.contains_point(x, y):
            return button.value
    return None


def _camera_size(capture) -> RenderSize:
    width = int(capture.get(3) or 640)
    height = int(capture.get(4) or 480)
    return RenderSize(width, height)


def _window_image_size(cv2, window_title: str) -> RenderSize | None:
    try:
        _x, _y, width, height = cv2.getWindowImageRect(window_title)
    except Exception:
        return None

    if width < 240 or height < 200:
        return None
    return RenderSize(width, height)


def _should_relayout(current_size: RenderSize, next_size: RenderSize | None) -> bool:
    if next_size is None:
        return False
    return abs((current_size.width or 0) - (next_size.width or 0)) >= 24 or abs(
        (current_size.height or 0) - (next_size.height or 0)
    ) >= 24
