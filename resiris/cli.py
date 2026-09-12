from __future__ import annotations

import argparse
from pathlib import Path

from .interpreter import Interpreter, RuntimeErrorResiris
from .parser import Parser, ast_to_dict
from .tokenizer import ResirisSyntaxError, Tokenizer


# ─────────────────────────────────────────────
# Terminal colors
# ─────────────────────────────────────────────

RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"


# ─────────────────────────────────────────────
# Resiris CLI banner
# ─────────────────────────────────────────────

BANNER = f"""{RED}
██████╗ ███████╗███████╗██╗██████╗ ██╗███████╗
██╔══██╗██╔════╝██╔════╝██║██╔══██╗██║██╔════╝
██████╔╝█████╗  ███████╗██║██████╔╝██║███████╗
██╔══██╗██╔══╝  ╚════██║██║██╔══██╗██║╚════██║
██║  ██║███████╗███████║██║██║  ██║██║███████║
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚══════╝
{RESET}"""


def print_banner() -> None:
    print(BANNER)
    print("Resiris Developer CLI v0.1")
    print()


# ─────────────────────────────────────────────
# Run .resy file
# ─────────────────────────────────────────────

def run_file(source_path: Path, show_frontend: bool = False) -> int:
    if source_path.suffix.lower() != ".resy":
        print(
            f"{RED}ResirisError:{RESET} "
            "Resiris files must have the .resy extension."
        )
        return 1

    if not source_path.is_file():
        print(
            f"{RED}ResirisError:{RESET} "
            f"file not found: {source_path}"
        )
        return 1

    try:
        source = source_path.read_text(encoding="utf-8")

        tokens = Tokenizer().tokenize(source)
        program = Parser(tokens).parse()

        Interpreter().run(program)

        if show_frontend:
            print()
            print("=== TOKENS ===")
            for token in tokens:
                print(token)

            print()
            print("=== AST ===")
            print(ast_to_dict(program))

    except (ResirisSyntaxError, RuntimeErrorResiris) as error:
        print(
            f"{RED}{type(error).__name__}:{RESET} {error}"
        )
        return 1

    except UnicodeDecodeError:
        print(
            f"{RED}ResirisError:{RESET} "
            f"file is not UTF-8 encoded: {source_path}"
        )
        return 1

    except OSError as error:
        print(
            f"{RED}ResirisError:{RESET} "
            f"file cannot be read: {error}"
        )
        return 1

    return 0


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="resiris",
        description="Resiris developer CLI",
    )

    frontend_group = parser.add_mutually_exclusive_group()

    frontend_group.add_argument(
        "--enable-frontend-visibility",
        action="store_true",
        help="Show tokenizer and parser output after running the .resy file",
    )

    frontend_group.add_argument(
        "--disable-frontend-visibility",
        action="store_true",
        help="Disable tokenizer and parser output after running the .resy file",
    )

    parser.add_argument(
        "file",
        nargs="?",
        help=".resy file to run",
    )

    args = parser.parse_args()

    # No file supplied.
    # Do NOT automatically run main.resy.
    if args.file is None:
        print_banner()

        print("Usage:")
        print("  resiris <file.resy>")
        print()

        print("Example:")
        print("  resiris main.resy")
        print()

        print(f"{BLUE}Options:{RESET}")
        print("  --enable-frontend-visibility")
        print("               Show tokenizer and parser output after running")
        print("  --disable-frontend-visibility")
        print("               Disable tokenizer and parser output")
        print("  --help       Show this help message")
        print("  --version    Show the Resiris version")

        return 0

    show_frontend = args.enable_frontend_visibility and not args.disable_frontend_visibility
    return run_file(Path(args.file), show_frontend)


if __name__ == "__main__":
    raise SystemExit(main())