from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase

from scripts.capture_screenshots import capture_screenshots


class ScreenshotOutputPathTests(SimpleTestCase):
    def test_rejects_output_outside_repository_without_creating_directory(self):
        with TemporaryDirectory() as temporary_directory:
            output_dir = Path(temporary_directory) / "screenshots"

            with self.assertRaisesRegex(ValueError, "inside the project directory"):
                capture_screenshots(output_dir, port=8000)

            self.assertFalse(output_dir.exists())
