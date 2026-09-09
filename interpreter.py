from __future__ import annotations

from dataclasses import dataclass

from ast_nodes import (
    Assignment,
    BinaryExpr,
    Declaration,
    ExpressionStmt,
    Literal,
    Name,
    Program,
    UnaryExpr,
)
from tokenizer import ResirisSyntaxError


class RuntimeErrorResiris(Exception):
    """Resiris futási idejű hiba."""


class UnknownVariableError(RuntimeErrorResiris):
    pass


class TypeErrorResiris(RuntimeErrorResiris):
    pass


class ConstantAssignmentError(RuntimeErrorResiris):
    pass


class MissingValueError(RuntimeErrorResiris):
    pass


@dataclass
class Variable:
    value: object
    type_name: str
    is_constant: bool = False


class Interpreter:
    """
    Az első minimális Resiris Interpreter.

    Jelenleg:
      - v deklaráció
      - c deklaráció
      - int / float / string / bool alapértékek
      - UnknownObject deklaráció
      - =
      - +=, -=, *=, /=
      - +, -, *, /, %
      - ==, !=, >, <, >=, <=
      - változónevek
      - literálok

    Szándékosan még NEM futtat:
      - if / elif / else
      - fn / return
      - mat
      - await
      - modulokat
    """

    def __init__(self):
        self.variables: dict[str, Variable] = {}

    def run(self, program: Program) -> dict[str, Variable]:
        for statement in program.statements:
            self.execute(statement)

        return self.variables

    def execute(self, statement):
        if isinstance(statement, Declaration):
            self.execute_declaration(statement)
            return

        if isinstance(statement, Assignment):
            self.execute_assignment(statement)
            return

        if isinstance(statement, ExpressionStmt):
            self.evaluate(statement.expression)
            return

        # A Parser már ismeri ezeket, de az első Interpreter még nem hajtja végre.
        # Így véletlenül sem úgy teszünk, mintha már támogatottak lennének.
        raise RuntimeErrorResiris(
            f"Az Interpreter jelenlegi verziója nem támogatja: "
            f"{type(statement).__name__}"
        )

    def execute_declaration(self, statement: Declaration):
        if statement.name in self.variables:
            raise RuntimeErrorResiris(
                f"{statement.name}: a név már használatban van"
            )

        if statement.value is None:
            if statement.type_name == "UnknownObject":
                raise MissingValueError(
                    f"{statement.name}: UnknownObject első értékadása szükséges"
                )

            raise MissingValueError(
                f"{statement.name}: a deklarációhoz jelenleg érték kell"
            )

        value = self.evaluate(statement.value)

        actual_type = statement.type_name

        # UnknownObject esetén az első értékadás dönti el
        # a tényleges Resiris típust.
        if statement.type_name == "UnknownObject":
            actual_type = self.infer_type_name(value)

        value = self.validate_and_coerce(
            actual_type,
            value,
            statement.name,
        )

        self.variables[statement.name] = Variable(
            value=value,
            type_name=actual_type,
            is_constant=(statement.kind == "c"),
        )

    def execute_assignment(self, statement: Assignment):
        variable = self.variables.get(statement.target)

        if variable is None:
            raise UnknownVariableError(
                f"{statement.target}: ismeretlen név"
            )

        if variable.is_constant:
            raise ConstantAssignmentError(
                f"{statement.target}: konstans nem módosítható"
            )

        right = self.evaluate(statement.value)

        if statement.operator == "=":
            new_value = right

        elif statement.operator == "+=":
            new_value = self.apply_binary(
                variable.value,
                "+",
                right,
                statement.target,
            )

        elif statement.operator == "-=":
            new_value = self.apply_binary(
                variable.value,
                "-",
                right,
                statement.target,
            )

        elif statement.operator == "*=":
            new_value = self.apply_binary(
                variable.value,
                "*",
                right,
                statement.target,
            )

        elif statement.operator == "/=":
            new_value = self.apply_binary(
                variable.value,
                "/",
                right,
                statement.target,
            )

        else:
            raise RuntimeErrorResiris(
                f"Ismeretlen értékadási operátor: {statement.operator}"
            )

        variable.value = self.validate_and_coerce(
            variable.type_name,
            new_value,
            statement.target,
        )

    def evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, Name):
            variable = self.variables.get(expression.name)

            if variable is None:
                raise UnknownVariableError(
                    f"{expression.name}: ismeretlen név"
                )

            return variable.value

        if isinstance(expression, UnaryExpr):
            value = self.evaluate(expression.operand)

            if expression.operator == "+":
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    raise TypeErrorResiris(
                        f"unáris + csak számra használható: {value!r}"
                    )

                return +value

            if expression.operator == "-":
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    raise TypeErrorResiris(
                        f"unáris - csak számra használható: {value!r}"
                    )

                return -value

            raise RuntimeErrorResiris(
                f"Ismeretlen unáris operátor: {expression.operator}"
            )

        if isinstance(expression, BinaryExpr):
            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)

            return self.apply_binary(
                left,
                expression.operator,
                right,
                None,
            )

        raise RuntimeErrorResiris(
            f"Az Interpreter jelenlegi verziója nem ismeri ezt a kifejezést: "
            f"{type(expression).__name__}"
        )

    def apply_binary(self, left, operator, right, target_name):
        # bool Pythonban az int leszármazottja,
        # ezért külön kezeljük.
        left_is_number = (
            isinstance(left, (int, float))
            and not isinstance(left, bool)
        )

        right_is_number = (
            isinstance(right, (int, float))
            and not isinstance(right, bool)
        )

        if operator in {"+", "-", "*", "/", "%"}:
            if not (left_is_number and right_is_number):
                raise TypeErrorResiris(
                    f"{operator}: numerikus operandusok szükségesek; "
                    f"kapott: {type(left).__name__}, "
                    f"{type(right).__name__}"
                )

            if operator == "+":
                return left + right

            if operator == "-":
                return left - right

            if operator == "*":
                return left * right

            if operator == "/":
                if right == 0:
                    raise RuntimeErrorResiris("nullával való osztás")

                return left / right

            if operator == "%":
                if right == 0:
                    raise RuntimeErrorResiris("nullával való modulo")

                return left % right

        if operator in {"==", "!=", ">", "<", ">=", "<="}:
            if operator == "==":
                return left == right

            if operator == "!=":
                return left != right

            if operator == ">":
                return left > right

            if operator == "<":
                return left < right

            if operator == ">=":
                return left >= right

            if operator == "<=":
                return left <= right

        raise RuntimeErrorResiris(
            f"Ismeretlen bináris operátor: {operator}"
        )

    def infer_type_name(self, value):
        if isinstance(value, bool):
            return "bool"

        if isinstance(value, int):
            return "int"

        if isinstance(value, float):
            return "float"

        if isinstance(value, str):
            return "string"

        raise TypeErrorResiris(
            f"UnknownObject: nem meghatározható típus: "
            f"{type(value).__name__}"
        )

    def validate_and_coerce(self, type_name, value, name):
        if type_name == "UnknownObject":
            # Az első értékadás dönti el a tényleges értéket/típust.
            return value

        if type_name == "int":
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeErrorResiris(
                    f"{name}: int érték szükséges, "
                    f"kapott: {type(value).__name__}"
                )

            return value

        if type_name == "float":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeErrorResiris(
                    f"{name}: float érték szükséges, "
                    f"kapott: {type(value).__name__}"
                )

            return float(value)

        if type_name == "string":
            if not isinstance(value, str):
                raise TypeErrorResiris(
                    f"{name}: string érték szükséges, "
                    f"kapott: {type(value).__name__}"
                )

            return value

        if type_name == "bool":
            if not isinstance(value, bool):
                raise TypeErrorResiris(
                    f"{name}: bool érték szükséges, "
                    f"kapott: {type(value).__name__}"
                )

            return value

        if type_name == "ResirisModuleObject":
            raise TypeErrorResiris(
                f"{name}: ResirisModuleObject kezelése még nincs implementálva"
            )

        raise RuntimeErrorResiris(
            f"{name}: ismeretlen típus: {type_name}"
        )