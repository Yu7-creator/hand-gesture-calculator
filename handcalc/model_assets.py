from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from urllib.request import urlretrieve


DEFAULT_HAND_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/latest/hand_landmarker.task"
)
DEFAULT_MODEL_PATH = Path("models") / "hand_landmarker.task"

Downloader = Callable[[str, Path], object]


def ensure_hand_model(
    model_path: str | Path | None = None,
    downloader: Downloader | None = None,
) -> Path:
    destination = Path(model_path) if model_path is not None else DEFAULT_MODEL_PATH
    destination = destination.expanduser()

    if destination.exists():
        return destination

    destination.parent.mkdir(parents=True, exist_ok=True)
    active_downloader = downloader or _download
    active_downloader(DEFAULT_HAND_MODEL_URL, destination)

    if not destination.exists():
        raise FileNotFoundError(f"Hand landmarker model was not created: {destination}")

    return destination


def _download(url: str, destination: Path) -> None:
    temp_destination = destination.with_suffix(destination.suffix + ".download")
    try:
        urlretrieve(url, temp_destination)
        temp_destination.replace(destination)
    finally:
        if temp_destination.exists():
            temp_destination.unlink()
