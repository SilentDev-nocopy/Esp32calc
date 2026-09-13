from pathlib import Path

from resiris.ast_nodes import Include, Program
from resiris.interpreter import Interpreter


def test_bundled_rsmath_metadata():
    project_root = Path(__file__).resolve().parents[1]
    interpreter = Interpreter(modules_dir=project_root / "Modules")
    interpreter.run(Program([Include(["RSMath"])]))

    info = interpreter.module_loader.info["RSMath"]
    assert info.name == "RSMath"
    assert info.functions == "sqrt"
    assert info.variables == ""
