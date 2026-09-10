from __future__ import annotations

from dataclasses import dataclass

from ast_nodes import (
    Assignment,
    BinaryExpr,
    CallExpr,
    Declaration,
    ExpressionStmt,
    FunctionDef,
    IfStmt,
    PrintCmdStmt,
    Literal,
    Name,
    Program,
    PassStmt,
    ReturnStmt,
    FunctionalObjectDef,
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


class FunctionError(RuntimeErrorResiris):
    pass


class ReturnSignal(Exception):
    """Belső jelzés a return végrehajtásához."""

    def __init__(self, value):
        super().__init__()
        self.value = value


@dataclass
class FunctionalObject:
    parameters: list[str]
    body: list[object]


@dataclass
class Variable:
    value: object
    type_name: str
    is_constant: bool = False


class Interpreter:
    """
    Resiris PC-s Interpreter prototípus.

    Jelenleg:
      - v / c deklaráció
      - int / float / string / bool
      - UnknownObject
      - =, +=, -=, *=, /=
      - +, -, *, /, %
      - ==, !=, >, <, >=, <=
      - változónevek
      - literálok
      - if / elif / else
      - fn
      - return
      - függvényhívás
      - print_cmd()

    Még NEM futtat:
      - mat
      - await
      - include
      - modulokat

    Scope:
      - a függvény paraméterei és a benne létrehozott v-k lokálisak
      - a globális v-k olvashatók a függvényből
      - ez a scope-szabály jelenleg PROTOTÍPUS, nem végleges Resiris-specifikáció
    """

    def __init__(self):
        self.variables: dict[str, Variable] = {}
        self.functions: dict[str, FunctionDef] = {}
        self.scope_stack: list[dict[str, Variable]] = []

    def run(self, program: Program) -> dict[str, Variable]:
        # A top-level függvénydefiníciókat előbb regisztráljuk,
        # így egy függvény a programban való későbbi helyéről is hívható.
        for statement in program.statements:
            if isinstance(statement, FunctionDef):
                self.register_function(statement)

        for statement in program.statements:
            if isinstance(statement, FunctionDef):
                continue

            self.execute(statement)

        return self.variables

    def register_function(self, statement: FunctionDef):
        if statement.name in self.functions:
            raise FunctionError(
                f"{statement.name}: a függvény már létezik"
            )

        if statement.name in self.variables:
            raise FunctionError(
                f"{statement.name}: a név már változóként használatban van"
            )

        self.functions[statement.name] = statement

    def execute(self, statement):
        if isinstance(statement, Declaration):
            self.execute_declaration(statement)
            return

        if isinstance(statement, Assignment):
            self.execute_assignment(statement)
            return

        if isinstance(statement, IfStmt):
            self.execute_if(statement)
            return

        if isinstance(statement, FunctionDef):
            return

        if isinstance(statement, ReturnStmt):
            self.execute_return(statement)
            return

        if isinstance(statement, PassStmt):
            return

        if isinstance(statement, PrintCmdStmt):
            self.execute_print_cmd(statement)
            return

        if isinstance(statement, ExpressionStmt):
            self.evaluate(statement.expression)
            return

        raise RuntimeErrorResiris(
            f"Az Interpreter jelenlegi verziója nem támogatja: "
            f"{type(statement).__name__}"
        )

    def execute_declaration(self, statement: Declaration):
        current_scope = self.current_scope()

        if statement.name in current_scope:
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

        if statement.type_name == "FunctionalObject":
            if not isinstance(statement.value, FunctionalObjectDef):
                raise TypeErrorResiris(
                    f"{statement.name}: FunctionalObject.new(...) szükséges"
                )
            value = FunctionalObject(statement.value.parameters, statement.value.body)
        else:
            value = self.evaluate(statement.value)

        actual_type = statement.type_name

        if statement.type_name == "UnknownObject":
            actual_type = self.infer_type_name(value)

        value = self.validate_and_coerce(
            actual_type,
            value,
            statement.name,
        )

        current_scope[statement.name] = Variable(
            value=value,
            type_name=actual_type,
            is_constant=(statement.kind == "c"),
        )

    def execute_assignment(self, statement: Assignment):
        variable = self.find_variable(statement.target)

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
                variable.value, "+", right, statement.target
            )

        elif statement.operator == "-=":
            new_value = self.apply_binary(
                variable.value, "-", right, statement.target
            )

        elif statement.operator == "*=":
            new_value = self.apply_binary(
                variable.value, "*", right, statement.target
            )

        elif statement.operator == "/=":
            new_value = self.apply_binary(
                variable.value, "/", right, statement.target
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

    def execute_if(self, statement: IfStmt):
        condition = self.evaluate(statement.condition)

        if not isinstance(condition, bool):
            raise TypeErrorResiris(
                "az if feltételének bool értéket kell adnia"
            )

        if condition:
            self.execute_block(statement.body)
            return

        for elif_condition, elif_body in statement.elif_blocks:
            condition = self.evaluate(elif_condition)

            if not isinstance(condition, bool):
                raise TypeErrorResiris(
                    "az elif feltételének bool értéket kell adnia"
                )

            if condition:
                self.execute_block(elif_body)
                return

        if statement.else_body is not None:
            self.execute_block(statement.else_body)

    def execute_block(self, statements):
        for statement in statements:
            self.execute(statement)

    def execute_return(self, statement: ReturnStmt):
        if not self.scope_stack:
            raise FunctionError(
                "`return` csak függvényen belül használható"
            )

        value = None
        if statement.value is not None:
            value = self.evaluate(statement.value)

        raise ReturnSignal(value)

    def execute_print_cmd(self, statement: PrintCmdStmt):
        value = self.evaluate(statement.expression)
        print(value)

    def call_function(self, function_name: str, arguments: list[object]):
        function = self.functions.get(function_name)

        if function is None:
            raise FunctionError(
                f"{function_name}: ismeretlen függvény"
            )

        if len(arguments) != len(function.parameters):
            raise FunctionError(
                f"{function_name}: {len(function.parameters)} paraméter szükséges, "
                f"de {len(arguments)} argumentum érkezett"
            )

        local_scope: dict[str, Variable] = {}

        for parameter_name, argument_value in zip(
            function.parameters,
            arguments,
        ):
            if parameter_name in local_scope:
                raise FunctionError(
                    f"{function_name}: duplikált paraméternév: {parameter_name}"
                )

            local_scope[parameter_name] = Variable(
                value=argument_value,
                type_name=self.infer_type_name(argument_value),
                is_constant=False,
            )

        self.scope_stack.append(local_scope)

        try:
            try:
                self.execute_block(function.body)
            except ReturnSignal as signal:
                return signal.value

            # A return nélküli függvény jelenlegi prototípusos eredménye:
            # None.
            return None

        finally:
            self.scope_stack.pop()

    def current_scope(self) -> dict[str, Variable]:
        if self.scope_stack:
            return self.scope_stack[-1]

        return self.variables

    def find_variable(self, name: str) -> Variable | None:
        if self.scope_stack:
            local_scope = self.scope_stack[-1]

            if name in local_scope:
                return local_scope[name]

        return self.variables.get(name)

    def evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, Name):
            variable = self.find_variable(expression.name)

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

        if isinstance(expression, CallExpr):
            arguments = [
                self.evaluate(argument)
                for argument in expression.arguments
            ]

            if isinstance(expression.function, Name):
                variable = self.find_variable(expression.function.name)
                if variable is not None and isinstance(variable.value, FunctionalObject):
                    return self.call_function_object(variable.value, arguments)

                return self.call_function(expression.function.name, arguments)

            raise FunctionError(
                "A függvényhívás célja jelenleg név vagy FunctionalObject kell legyen"
            )

        raise RuntimeErrorResiris(
            f"Az Interpreter jelenlegi verziója nem ismeri ezt a kifejezést: "
            f"{type(expression).__name__}"
        )


    def call_function_object(self, function: FunctionalObject, arguments: list[object]):
        if len(arguments) != len(function.parameters):
            raise FunctionError(
                f"FunctionalObject: {len(function.parameters)} paraméter szükséges, "
                f"de {len(arguments)} argumentum érkezett"
            )

        local_scope: dict[str, Variable] = {}
        for parameter_name, argument_value in zip(function.parameters, arguments):
            if parameter_name in local_scope:
                raise FunctionError(
                    f"FunctionalObject: duplikált paraméternév: {parameter_name}"
                )
            local_scope[parameter_name] = Variable(
                value=argument_value,
                type_name=self.infer_type_name(argument_value),
                is_constant=False,
            )

        self.scope_stack.append(local_scope)
        try:
            try:
                self.execute_block(function.body)
            except ReturnSignal as signal:
                return signal.value
            return None
        finally:
            self.scope_stack.pop()

    def apply_binary(self, left, operator, right, target_name):
        left_is_number = (
            isinstance(left, (int, float))
            and not isinstance(left, bool)
        )

        right_is_number = (
            isinstance(right, (int, float))
            and not isinstance(right, bool)
        )

        if operator == "+":
            if isinstance(left, str) and isinstance(right, str):
                return left + right

            if not (left_is_number and right_is_number):
                raise TypeErrorResiris(
                    f"+: azonos típusú stringek vagy numerikus operandusok szükségesek; "
                    f"kapott: {type(left).__name__}, {type(right).__name__}"
                )

            return left + right

        if operator in {"-", "*", "/", "%"}:
            if not (left_is_number and right_is_number):
                raise TypeErrorResiris(
                    f"{operator}: numerikus operandusok szükségesek; "
                    f"kapott: {type(left).__name__}, "
                    f"{type(right).__name__}"
                )

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

        if type_name == "FunctionalObject":
            if not isinstance(value, FunctionalObject):
                raise TypeErrorResiris(
                    f"{name}: FunctionalObject érték szükséges, kapott: {type(value).__name__}"
                )
            return value

        if type_name == "ResirisModuleObject":
            raise TypeErrorResiris(
                f"{name}: ResirisModuleObject kezelése még nincs implementálva"
            )

        raise RuntimeErrorResiris(
            f"{name}: ismeretlen típus: {type_name}"
        )
