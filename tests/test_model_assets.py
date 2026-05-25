import tempfile
import unittest
from pathlib import Path

from handcalc.model_assets import DEFAULT_HAND_MODEL_URL, ensure_hand_model


class ModelAssetTests(unittest.TestCase):
    def test_ensure_hand_model_returns_existing_file_without_download(self):
        with tempfile.TemporaryDirectory() as tmp:
            model = Path(tmp) / "hand_landmarker.task"
            model.write_bytes(b"existing")

            resolved = ensure_hand_model(model_path=model, downloader=self.fail)

            self.assertEqual(resolved, model)

    def test_ensure_hand_model_downloads_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            model = Path(tmp) / "hand_landmarker.task"
            calls = []

            def downloader(url, destination):
                calls.append((url, destination))
                destination.write_bytes(b"downloaded")

            resolved = ensure_hand_model(model_path=model, downloader=downloader)

            self.assertEqual(resolved, model)
            self.assertEqual(model.read_bytes(), b"downloaded")
            self.assertEqual(calls, [(DEFAULT_HAND_MODEL_URL, model)])


if __name__ == "__main__":
    unittest.main()
