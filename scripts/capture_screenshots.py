from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import URLError
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
MANAGE_PY = ROOT / "simple_url_shortner" / "manage.py"


def _ensure_port_available(port: int) -> None:
    with socket.socket() as server_socket:
        try:
            server_socket.bind(("127.0.0.1", port))
        except OSError as exc:
            raise RuntimeError(
                f"Port {port} is unavailable; pass another port with --port."
            ) from exc


def _wait_for_server(
    process: subprocess.Popen[bytes], url: str, log_path: Path
) -> None:
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if process.poll() is not None:
            server_output = log_path.read_text(encoding="utf-8")
            raise RuntimeError(f"Development server exited early:\n{server_output}")
        try:
            with urlopen(url, timeout=1):
                return
        except (URLError, TimeoutError):
            time.sleep(0.25)
    raise TimeoutError(
        f"Development server did not start in time:\n"
        f"{log_path.read_text(encoding='utf-8')}"
    )


def capture_screenshots(output_dir: Path, port: int) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    _ensure_port_available(port)
    base_url = f"http://127.0.0.1:{port}/"

    with TemporaryDirectory(prefix="urlshortener-e2e-") as temp_dir:
        temp_path = Path(temp_dir)
        database_path = temp_path / "e2e.sqlite3"
        server_log = temp_path / "server.log"
        environment = os.environ.copy()
        environment.update(
            {
                "DJANGO_DEBUG": "true",
                "DJANGO_SECRET_KEY": "e2e-only-development-key",
                "DJANGO_ALLOWED_HOSTS": "127.0.0.1,localhost",
                "DJANGO_DB_PATH": str(database_path),
            }
        )

        subprocess.run(
            [sys.executable, str(MANAGE_PY), "migrate", "--noinput"],
            cwd=ROOT,
            env=environment,
            check=True,
        )

        with server_log.open("w", encoding="utf-8") as log_file:
            server = subprocess.Popen(
                [
                    sys.executable,
                    str(MANAGE_PY),
                    "runserver",
                    f"127.0.0.1:{port}",
                    "--noreload",
                ],
                cwd=ROOT,
                env=environment,
                stdout=log_file,
                stderr=subprocess.STDOUT,
            )
            try:
                _wait_for_server(server, base_url, server_log)
                screenshots = [
                    output_dir / "home.png",
                    output_dir / "shortened-url.png",
                ]
                with sync_playwright() as playwright:
                    browser = playwright.chromium.launch()
                    try:
                        page = browser.new_page(
                            viewport={"width": 1440, "height": 1000},
                            device_scale_factor=1,
                        )
                        response = page.goto(base_url, wait_until="networkidle")
                        if response is None or response.status != 200:
                            raise RuntimeError("The home page did not return HTTP 200.")
                        page.screenshot(path=str(screenshots[0]), full_page=True)

                        page.locator('input[name="original_url"]').fill(
                            "https://example.com/python"
                        )
                        page.get_by_role("button", name="Shorten URL").click()
                        page.get_by_text("URL was minified successfully.").wait_for()
                        page.screenshot(path=str(screenshots[1]), full_page=True)

                        short_url = page.locator("h3 a").get_attribute("href")
                        if not short_url:
                            raise AssertionError(
                                "The shortened URL link was not rendered."
                            )
                        redirect_response = page.request.get(
                            short_url,
                            max_redirects=0,
                        )
                        if (
                            redirect_response.status != 301
                            or redirect_response.headers.get("location")
                            != "https://example.com/python"
                        ):
                            raise AssertionError(
                                "The generated URL did not redirect to its destination."
                            )
                    finally:
                        browser.close()
                return screenshots
            finally:
                if server.poll() is None:
                    server.terminate()
                    try:
                        server.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        server.kill()
                        server.wait()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a Playwright smoke test and capture project screenshots."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "docs" / "screenshots",
        help="Directory for generated PNG screenshots.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Local port for the temporary Django server.",
    )
    arguments = parser.parse_args()

    for screenshot in capture_screenshots(
        arguments.output_dir.resolve(),
        arguments.port,
    ):
        print(f"Captured {screenshot}")


if __name__ == "__main__":
    main()
