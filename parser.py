from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Optional

from tokenizer import Token, TokenType, ResirisSyntaxError
from ast_nodes import (
    Program, Include, Declaration, FunctionDef, IfStmt, ReturnStmt, PassStmt,
    AwaitStmt, Assignment, ExpressionStmt, Literal, Name, UnaryExpr,
    BinaryExpr, CallExpr,
)


class Parser:
    """
    Resiris parser for the currently defined core grammar.

    It builds an AST. It does NOT execute code.
    """

    TYPE_TOKENS = {
        TokenType.TYPE_UNKNOWN: "UnknownObject",
        TokenType.TYPE_INT: "int",
        TokenType.TYPE_FLOAT: "float",
        TokenType.TYPE_STRING: "string",
        TokenType.TYPE_BOOL: "bool",
        TokenType.TYPE_RESIRIS_MODULE_OBJECT: "ResirisModuleObject",
    }

    ASSIGNMENT_TOKENS = {
        TokenType.ASSIGN: "=",
        TokenType.PLUS_ASSIGN: "+=",
        TokenType.MINUS_ASSIGN: "-=",
        TokenType.STAR_ASSIGN: "*=",
        TokenType.SLASH_ASSIGN: "/=",
    }

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def previous(self) -> Token:
        return self.tokens[self.pos - 1]

    def at(self, token_type: TokenType) -> bool:
        return self.current().type is token_type

    def advance(self) -> Token:
        token = self.current()
        if token.type is not TokenType.EOF:
            self.pos += 1
        return token

    def match(self, *types: TokenType) -> Optional[Token]:
        if self.current().type in types:
            return self.advance()
        return None

    def expect(self, token_type: TokenType, message: str) -> Token:
        token = self.current()
        if token.type is not token_type:
            self.error(token, message)
        return self.advance()

    def error(self, token: Token, message: str) -> None:
        raise ResirisSyntaxError(
            f"{token.line}:{token.column}: {message}; kapott: "
            f"{token.type.name} ({token.value!r})"
        )

    def parse(self) -> Program:
        statements = []
        self.skip_newlines()

        while not self.at(TokenType.EOF):
            statements.append(self.parse_statement())
            self.skip_newlines()

        return Program(statements)

    def skip_newlines(self) -> None:
        while self.match(TokenType.NEWLINE):
            pass

    def parse_statement(self):
        token = self.current()

        if token.type is TokenType.INCLUDE:
            return self.parse_include()
        if token.type in (TokenType.V, TokenType.C):
            return self.parse_declaration()
        if token.type is TokenType.FN:
            return self.parse_function()
        if token.type in (TokenType.START, TokenType.PROCESS):
            return self.parse_named_function()
        if token.type is TokenType.IF:
            return self.parse_if()
        if token.type is TokenType.MAT:
            self.error(
                token,
                "a `mat` tokenizálva van, de a case/ág szintaxisa jelenleg nincs "
                "egyértelműen definiálva a specifikációban"
            )
        if token.type is TokenType.RETURN:
            return self.parse_return()
        if token.type is TokenType.PASS:
            self.advance()
            self.expect(TokenType.NEWLINE, "a `pass` után sorvége kell")
            return PassStmt()
        if token.type is TokenType.AWAIT:
            self.advance()
            expression = self.parse_expression()
            self.expect(TokenType.NEWLINE, "az `await` után sorvége kell")
            return AwaitStmt(expression)

        return self.parse_assignment_or_expression()

    def parse_include(self) -> Include:
        self.advance()
        module = self.expect(
            TokenType.IDENTIFIER,
            "az `include` után modulnév kell"
        )
        self.expect(TokenType.NEWLINE, "az `include` után sorvége kell")
        return Include(module.value)

    def parse_declaration(self) -> Declaration:
        kind = self.advance().value
        name = self.expect(
            TokenType.IDENTIFIER,
            "a deklarációban az első névnek azonosítónak kell lennie"
        )

        type_token = self.current()
        if type_token.type not in self.TYPE_TOKENS:
            self.error(
                type_token,
                "a deklarációban típusnév kell"
            )
        type_name = self.TYPE_TOKENS[self.advance().type]

        value = None
        if self.match(TokenType.ASSIGN):
            value = self.parse_expression()

        self.expect(TokenType.NEWLINE, "a deklaráció végén sorvége kell")
        return Declaration(kind, name.value, type_name, value)

    def parse_function(self) -> FunctionDef:
        self.advance()  # fn
        name = self.expect(TokenType.IDENTIFIER, "az `fn` után függvénynév kell")
        parameters = self.parse_parameter_list()
        self.expect(TokenType.COLON, "a függvény fejlécének végén `:` kell")
        self.expect(TokenType.NEWLINE, "a `:` után sorvége kell")
        body = self.parse_block()
        return FunctionDef(name.value, parameters, body)

    def parse_named_function(self) -> FunctionDef:
        name_token = self.advance()
        parameters = self.parse_parameter_list()
        self.expect(TokenType.COLON, "a függvény fejlécének végén `:` kell")
        self.expect(TokenType.NEWLINE, "a `:` után sorvége kell")
        body = self.parse_block()
        return FunctionDef(name_token.value, parameters, body)

    def parse_parameter_list(self) -> list[str]:
        self.expect(TokenType.LPAREN, "a függvény neve után `(` kell")
        parameters: list[str] = []

        if not self.at(TokenType.RPAREN):
            while True:
                param = self.expect(
                    TokenType.IDENTIFIER,
                    "a függvény paraméterének azonosítónak kell lennie"
                )
                parameters.append(param.value)
                if not self.match(TokenType.COMMA):
                    break

        self.expect(TokenType.RPAREN, "hiányzó `)` a paraméterlistában")
        return parameters

    def parse_block(self) -> list[object]:
        self.expect(TokenType.INDENT, "a blokkhoz behúzott sor kell")
        self.skip_newlines()

        statements = []
        while not self.at(TokenType.DEDENT) and not self.at(TokenType.EOF):
            statements.append(self.parse_statement())
            self.skip_newlines()

        self.expect(TokenType.DEDENT, "hiányzó blokkzárás")
        return statements

    def parse_if(self) -> IfStmt:
        self.advance()  # if
        condition = self.parse_expression()
        self.expect(TokenType.COLON, "az `if` végén `:` kell")
        self.expect(TokenType.NEWLINE, "az `if` után sorvége kell")
        body = self.parse_block()

        elif_blocks = []
        while self.match(TokenType.ELIF):
            elif_condition = self.parse_expression()
            self.expect(TokenType.COLON, "az `elif` végén `:` kell")
            self.expect(TokenType.NEWLINE, "az `elif` után sorvége kell")
            elif_body = self.parse_block()
            elif_blocks.append((elif_condition, elif_body))

        else_body = None
        if self.match(TokenType.ELSE):
            self.expect(TokenType.COLON, "az `else` végén `:` kell")
            self.expect(TokenType.NEWLINE, "az `else` után sorvége kell")
            else_body = self.parse_block()

        return IfStmt(condition, body, elif_blocks, else_body)

    def parse_return(self) -> ReturnStmt:
        self.advance()
        if self.at(TokenType.NEWLINE):
            self.advance()
            return ReturnStmt(None)

        value = self.parse_expression()
        self.expect(TokenType.NEWLINE, "a `return` végén sorvége kell")
        return ReturnStmt(value)

    def parse_assignment_or_expression(self):
        expression = self.parse_expression()

        if isinstance(expression, Name) and self.current().type in self.ASSIGNMENT_TOKENS:
            operator = self.ASSIGNMENT_TOKENS[self.advance().type]
            value = self.parse_expression()
            self.expect(TokenType.NEWLINE, "az értékadás végén sorvége kell")
            return Assignment(expression.name, operator, value)

        self.expect(TokenType.NEWLINE, "a kifejezés végén sorvége kell")
        return ExpressionStmt(expression)

    # Expression precedence:
    # comparison
    # addition/subtraction
    # multiplication/division/modulo
    # unary
    # call / primary

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        expr = self.parse_term()

        while self.current().type in {
            TokenType.EQ, TokenType.NE, TokenType.GT, TokenType.LT,
            TokenType.GE, TokenType.LE,
        }:
            op = self.advance().value
            right = self.parse_term()
            expr = BinaryExpr(expr, op, right)

        return expr

    def parse_term(self):
        expr = self.parse_factor()

        while self.current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_factor()
            expr = BinaryExpr(expr, op, right)

        return expr

    def parse_factor(self):
        expr = self.parse_unary()

        while self.current().type in (
            TokenType.STAR, TokenType.SLASH, TokenType.PERCENT
        ):
            op = self.advance().value
            right = self.parse_unary()
            expr = BinaryExpr(expr, op, right)

        return expr

    def parse_unary(self):
        if self.match(TokenType.PLUS):
            return UnaryExpr("+", self.parse_unary())
        if self.match(TokenType.MINUS):
            return UnaryExpr("-", self.parse_unary())
        return self.parse_call()

    def parse_call(self):
        expr = self.parse_primary()

        while self.match(TokenType.LPAREN):
            arguments = []
            if not self.at(TokenType.RPAREN):
                while True:
                    arguments.append(self.parse_expression())
                    if not self.match(TokenType.COMMA):
                        break
            self.expect(TokenType.RPAREN, "hiányzó `)` a hívásban")
            expr = CallExpr(expr, arguments)

        return expr

    def parse_primary(self):
        token = self.current()

        if token.type is TokenType.INTEGER:
            self.advance()
            return Literal(token.value)

        if token.type is TokenType.FLOAT:
            self.advance()
            return Literal(token.value)

        if token.type is TokenType.STRING:
            self.advance()
            return Literal(token.value)

        if token.type is TokenType.IDENTIFIER:
            self.advance()
            return Name(token.value)

        if token.type is TokenType.START:
            self.advance()
            return Name("start")

        if token.type is TokenType.PROCESS:
            self.advance()
            return Name("process")

        if token.type in self.TYPE_TOKENS:
            self.error(
                token,
                "a típusnév itt nem kifejezés"
            )

        self.error(token, "érvényes kifejezés várt")
        raise AssertionError("unreachable")


def ast_to_dict(node):
    """Kis debug helper: az AST könnyen kiírható JSON-szerű dictként."""
    if is_dataclass(node):
        result = {}
        for key, value in asdict(node).items():
            result[key] = value
        return result
    return node
