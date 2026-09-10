from __future__ import annotations

import argparse
from pathlib import Path

from .interpreter import Interpreter, RuntimeErrorResiris
from .parser import Parser
from .tokenizer import ResirisSyntaxError, Tokenizer


def run_file(source_path: Path) -> int:
    if source_path.suffix.lower() != ".resy":
        print("ResirisError: a Resiris fájlok kiterjesztése .resy kell legyen.")
        return 1

    if not source_path.is_file():
        print(f"ResirisError: a fájl nem található: {source_path}")
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
        print(f"ResirisError: a fájl nem UTF-8 kódolású: {source_path}")
        return 1
    except OSError as error:
        print(f"ResirisError: a fájl nem olvasható: {error}")
        return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="resiris",
        description="Resiris fejlesztői parancssor",
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="futtatandó .resy fájl",
    )
    args = parser.parse_args()

    if args.file is None:
        print("Resiris v0.1")
        print("Resiris fejlesztői parancssor")
        print()
        print("Használat:")
        print("  resiris <fájl.resy>")
        print()
        print("Példa:")
        print("  resiris main.resy")
        return 0

    return run_file(Path(args.file))


if __name__ == "__main__":
    raise SystemExit(main())
