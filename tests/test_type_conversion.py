import pytest

from resiris.ast_nodes import TypeConversionExpr
from resiris.interpreter import Interpreter, TypeErrorResiris
from resiris.parser import Parser
from resiris.tokenizer import Tokenizer


def run(source):
    tokens = Tokenizer().tokenize(source)
    program = Parser(tokens).parse()
    return Interpreter().run(program)


def test_type_converts_int_to_float_without_modifying_original():
    variables = run("""\
v x int = 10
v y float = x.type(float)
""")

    assert variables["x"].value == 10
    assert variables["x"].type_name == "int"
    assert variables["y"].value == 10.0
    assert variables["y"].type_name == "float"


def test_type_converts_positive_number_to_true_without_modifying_original():
    variables = run("""\
v y float = 2
v z bool = y.type(bool)
""")
    assert variables["y"].value == 2.0
    assert variables["y"].type_name == "float"
    assert variables["z"].value is True
    assert variables["z"].type_name == "bool"


def test_type_bool_uses_greater_than_zero_for_numbers():
    variables = run("""\
v a int = 0
v b int = -3
v c int = 4
v aa bool = a.type(bool)
v bb bool = b.type(bool)
v cc bool = c.type(bool)
""")
    assert variables["aa"].value is False
    assert variables["bb"].value is False
    assert variables["cc"].value is True


def test_type_requires_exactly_one_builtin_type_argument():
    with pytest.raises(Exception):
        run("v x int = 10\nv y float = x.type()\n")

    with pytest.raises(Exception):
        run("v x int = 10\nv y float = x.type(float, int)\n")


def test_type_rejects_non_builtin_type_argument():
    with pytest.raises(Exception):
        run("v x int = 10\nv y float = x.type(UnknownObject)\n")


def test_type_string_conversion():
    variables = run("""\
v x int = 10
v y string = x.type(string)
""")
    assert variables["y"].value == "10"
    assert variables["y"].type_name == "string"
