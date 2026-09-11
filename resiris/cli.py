from __future__ import annotations

import argparse
from pathlib import Path

from .interpreter import Interpreter, RuntimeErrorResiris
from .parser import Parser
from .tokenizer import ResirisSyntaxError, Tokenizer


def run_file(source_path: Path) -> int:
    if source_path.suffix.lower() != ".resy":
        print("ResirisError: Resiris files must have the .resy extension.")
        return 1

    if not source_path.is_file():
        print(f"ResirisError: file not found: {source_path}")
        return 1

    try:
        source = source_path.read_text(encoding="utf-8")
        tokens = Tokenizer().tokenize(source)
        program = Parser(tokens).parse()
        Interpreter().run(program)
    except (ResirisSyntaxError, RuntimeErrorResiris) as error:
        print(f"{type(error).__name__}: {error}")
        return 1
    except UnicodeDecodeError:
        print(f"ResirisError: file is not UTF-8 encoded: {source_path}")
        return 1
    except OSError as error:
        print(f"ResirisError: file cannot be read: {error}")
        return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="resiris",
        description="Resiris developer CLI",
    )
    parser.add_argument(
        "file",
        nargs="?",
        help=".resy file to run",
    )
    args = parser.parse_args()

    if args.file is None:
        print("Resiris v0.1")
        print("Resiris developer CLI")
        print()
        print("Usage:")
        print("  resiris <file.resy>")
        print()
        print("Example:")
        print("  resiris main.resy")
        return 0

    return run_file(Path(args.file))


if __name__ == "__main__":
    raise SystemExit(main())
