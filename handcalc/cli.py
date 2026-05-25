from __future__ import annotations

import argparse

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m handcalc",
        description="Run the local hand-gesture calculator demo.",
    )
    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="OpenCV camera index to use. Default: 0.",
    )
    parser.add_argument(
        "--click-delay",
        type=float,
        default=0.75,
        help="Minimum seconds between pinch clicks. Default: 0.75.",
    )
    parser.add_argument(
        "--pinch-threshold",
        type=float,
        default=40.0,
        help="Maximum thumb/index distance for a click. Default: 40.",
    )
    parser.add_argument(
        "--model-path",
        default=None,
        help="Path to a MediaPipe hand_landmarker.task model. Default: models/hand_landmarker.task.",
    )
    parser.add_argument(
        "--frame-width",
        type=int,
        default=None,
        help="Initial rendered OpenCV frame width. Default: auto-detect from the screen.",
    )
    parser.add_argument(
        "--frame-height",
        type=int,
        default=None,
        help="Initial rendered OpenCV frame height. Default: auto-detect from the screen.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    from .app import AppConfig, run

    config = AppConfig(
        camera_index=args.camera_index,
        click_delay=args.click_delay,
        pinch_threshold=args.pinch_threshold,
        model_path=args.model_path,
        frame_width=args.frame_width,
        frame_height=args.frame_height,
    )
    return run(config)
