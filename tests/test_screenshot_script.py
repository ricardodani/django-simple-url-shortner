import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "capture_screenshots.py"
SPEC = importlib.util.spec_from_file_location(
    "scripts.capture_screenshots",
    SCRIPT_PATH,
)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Could not import screenshot helper from {SCRIPT_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
capture_screenshots = MODULE.capture_screenshots


class ScreenshotOutputPathTests(SimpleTestCase):
    def test_main_passes_headed_option_to_screenshot_runner(self):
        with (
            patch.object(
                MODULE,
                "capture_screenshots",
                return_value=[],
            ) as capture_screenshots,
            patch(
                "sys.argv",
                ["capture_screenshots.py", "--headed"],
            ),
        ):
            MODULE.main()

        capture_screenshots.assert_called_once_with(
            MODULE.ROOT / "docs" / "screenshots",
            8000,
            headed=True,
        )

    def test_rejects_output_outside_repository_without_creating_directory(self):
        with TemporaryDirectory() as temporary_directory:
            output_dir = Path(temporary_directory) / "screenshots"

            with self.assertRaisesRegex(ValueError, "inside the project directory"):
                capture_screenshots(output_dir, port=8000)

            self.assertFalse(output_dir.exists())
