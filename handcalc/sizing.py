from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RenderSize:
    width: int | None
    height: int | None


def choose_render_size(
    camera_size: tuple[int, int] | RenderSize,
    screen_size: tuple[int, int] | RenderSize | None = None,
    requested_size: RenderSize | None = None,
) -> RenderSize:
    camera_width, camera_height = _coerce_size(camera_size, fallback=(960, 720))
    aspect = camera_width / camera_height if camera_width > 0 and camera_height > 0 else 4 / 3

    if screen_size is None:
        max_width, max_height = 1280, 900
    else:
        screen_width, screen_height = _coerce_size(screen_size, fallback=(1280, 900))
        max_width = min(screen_width, max(240, int(screen_width * 0.92)))
        max_height = min(screen_height, max(180, int(screen_height * 0.82)))

    requested_width = requested_size.width if requested_size else None
    requested_height = requested_size.height if requested_size else None

    if requested_width is not None and requested_height is not None:
        return _even_size(min(requested_width, max_width), min(requested_height, max_height))

    if requested_width is not None:
        width = min(requested_width, max_width)
        height = round(width / aspect)
        if height > max_height:
            height = max_height
            width = round(height * aspect)
        return _even_size(width, height)

    if requested_height is not None:
        height = min(requested_height, max_height)
        width = round(height * aspect)
        if width > max_width:
            width = max_width
            height = round(width / aspect)
        return _even_size(width, height)

    width = max_width
    height = round(width / aspect)
    if height > max_height:
        height = max_height
        width = round(height * aspect)

    return _even_size(width, height)


def detect_screen_size() -> RenderSize | None:
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
        try:
            return RenderSize(root.winfo_screenwidth(), root.winfo_screenheight())
        finally:
            root.destroy()
    except Exception:
        return None


def _coerce_size(size: tuple[int, int] | RenderSize, fallback: tuple[int, int]) -> tuple[int, int]:
    if isinstance(size, RenderSize):
        width = size.width
        height = size.height
    else:
        width, height = size

    return (width or fallback[0], height or fallback[1])


def _even_size(width: int, height: int) -> RenderSize:
    safe_width = max(240, int(width))
    safe_height = max(180, int(height))
    safe_width -= safe_width % 2
    safe_height -= safe_height % 2
    return RenderSize(safe_width, safe_height)
