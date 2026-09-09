from pathlib import Path

from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter


def main():
    source_path = Path("main.resy")
    source = source_path.read_text(encoding="utf-8")

    tokens = Tokenizer().tokenize(source)
    program = Parser(tokens).parse()

    interpreter = Interpreter()
    variables = interpreter.run(program)

    print("=== RESIRIS RUNTIME ===")
    for name, variable in variables.items():
        print(f"{name} = {variable.value!r} ({variable.type_name})")


if __name__ == "__main__":
    main()
