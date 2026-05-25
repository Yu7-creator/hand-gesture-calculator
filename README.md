# Hand Gesture Calculator

A local Python desktop demo that turns thumb-and-index pinch gestures into calculator input. It uses OpenCV for the webcam window and MediaPipe for hand landmark tracking, while the calculator logic stays isolated and unit-tested.

## Features

- Touchless 4x4 calculator UI for digits, `+`, `-`, `*`, `/`, clear, and equals.
- Pinch-to-click interaction with configurable threshold and cooldown.
- Safe arithmetic evaluator with no Python `eval()`.
- Automatic window sizing that fits the screen and keeps the calculator centered.
- MediaPipe Tasks support with automatic hand model download on first run.
- Unit-tested calculator state, expression evaluation, layout, gesture detection, and sizing logic.

## Requirements

- Python 3.11 or 3.12
- A webcam
- Internet access on first run to download `models/hand_landmarker.task`

The tests and CLI help command do not require a webcam.

## Quick Start

### Windows PowerShell

```powershell
git clone https://github.com/Yu7-creator/hand-gesture-calculator.git
cd hand-gesture-calculator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m handcalc
```

### macOS and Linux

```bash
git clone https://github.com/Yu7-creator/hand-gesture-calculator.git
cd hand-gesture-calculator
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m handcalc
```

Press `q` in the OpenCV window to quit.

## Useful Commands

```bash
python -m handcalc --help
python -m handcalc --camera-index 1
python -m handcalc --pinch-threshold 35 --click-delay 0.6
python -m handcalc --frame-width 960 --frame-height 720
python -m unittest discover -s tests -v
```

If editable install is not desired, use the fallback dependency install:

```bash
python -m pip install -r requirements.txt
```

## Demo Script

1. Start with your hand visible in the camera frame.
2. Move the pinch point over a key.
3. Pinch thumb and index finger to click.
4. Enter `7`, `*`, `6`, then `=` to show `42`.
5. Press `C`, then try division by zero to show the safe error state.
6. Press `q` to exit cleanly.

## Troubleshooting

- **No camera opens:** try `python -m handcalc --camera-index 1`.
- **Camera permission denied on Windows:** enable camera access in Settings > Privacy & security > Camera.
- **Camera permission denied on macOS:** allow Terminal or your IDE in System Settings > Privacy & Security > Camera.
- **Linux camera permission denied:** make sure your user can access `/dev/video*`; many distributions use the `video` group.
- **Linux OpenCV window problems:** install your distribution's desktop GUI/OpenGL packages, then rerun the app from a graphical session.
- **Model download blocked:** download the MediaPipe hand landmarker model manually and run `python -m handcalc --model-path path/to/hand_landmarker.task`.

## Project Layout

```text
handcalc/        application package
tests/           webcam-free unit tests
requirements.txt simple dependency fallback
pyproject.toml   package metadata and editable install support
```

## License

MIT
