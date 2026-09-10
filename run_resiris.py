from pathlib import Path
import sys

from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter


def main():
    if len(sys.argv) > 2:
        print("Usage: python3 run_resiris.py [file.resy]", file=sys.stderr)
        return 1

    source_path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("main.resy")

    if source_path.suffix.lower() != ".resy":
        print("Error: Resiris files must use the .resy extension.", file=sys.stderr)
        return 1

    if not source_path.is_file():
        print(f"Error: Resiris file not found: {source_path}", file=sys.stderr)
        return 1
    source = source_path.read_text(encoding="utf-8")

    tokens = Tokenizer().tokenize(source)
    program = Parser(tokens).parse()

    interpreter = Interpreter()
    variables = interpreter.run(program)

    print("=== RESIRIS RUNTIME ===")

    for name, variable in variables.items():
        print(f"{name} = {variable.value!r} ({variable.type_name})")


if __name__ == "__main__":
    raise SystemExit(main())
