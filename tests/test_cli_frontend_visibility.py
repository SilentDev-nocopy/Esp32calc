import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "main.resy"


def run(*args):
    return subprocess.run(
        [sys.executable, "-m", "resiris", *args, str(MAIN)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def main():
    enabled = run("--enable-frontend-visibility")
    if enabled.returncode != 0:
        raise SystemExit(enabled.stderr or enabled.stdout)
    if "=== TOKENS ===" not in enabled.stdout:
        raise SystemExit("Missing token frontend output")
    if "=== AST ===" not in enabled.stdout:
        raise SystemExit("Missing AST frontend output")

    disabled = run("--disable-frontend-visibility")
    if disabled.returncode != 0:
        raise SystemExit(disabled.stderr or disabled.stdout)
    if "=== TOKENS ===" in disabled.stdout:
        raise SystemExit("Frontend output was not disabled")
    if "=== AST ===" in disabled.stdout:
        raise SystemExit("Frontend output was not disabled")

    both = run("--enable-frontend-visibility", "--disable-frontend-visibility")
    if both.returncode == 0:
        raise SystemExit("Enable and disable flags should be mutually exclusive")
    if "usage:" in both.stdout.lower() or "usage:" in both.stderr.lower():
        raise SystemExit("Invalid CLI arguments should not print the full usage page")

    invalid = run("--not-a-real-option")
    if invalid.returncode == 0:
        raise SystemExit("Unknown CLI option should fail")
    if "usage:" in invalid.stdout.lower() or "usage:" in invalid.stderr.lower():
        raise SystemExit("Invalid CLI option should not print the full usage page")


if __name__ == "__main__":
    main()
