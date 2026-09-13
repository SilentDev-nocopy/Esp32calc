from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Optional

from .tokenizer import Token, TokenType, ResirisSyntaxError
from .ast_nodes import (
    Program, Include, Declaration, FunctionDef, IfStmt, ReturnStmt, PassStmt,
    AwaitStmt, PrintCmdStmt, Assignment, ExpressionStmt, Literal, Name, UnaryExpr,
    BinaryExpr, CallExpr, FunctionalObjectDef, TypeConversionExpr,
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
        TokenType.TYPE_FUNCTIONAL_OBJECT: "FunctionalObject",
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
        """Parse one statement and attach its source position to the AST node."""
        token = self.current()
        statement = self._parse_statement_impl()
        statement.source_line = token.line
        statement.source_column = token.column
        return statement

    def _parse_statement_impl(self):
        token = self.current()

        if token.type is TokenType.LT and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type is TokenType.INCLUDE:
            return self.parse_include()
        if token.type is TokenType.V:
            return self.parse_declaration()
        if token.type is TokenType.C:
            return self.parse_declaration()
        # `c` is a valid identifier for a varint.
        # Constant declaration is recognized by its declaration shape:
        # c <identifier> <type> [= expression]
        if (
            token.type is TokenType.IDENTIFIER
            and token.value == "c"
            and self.pos + 2 < len(self.tokens)
            and self.tokens[self.pos + 1].type is TokenType.IDENTIFIER
            and self.tokens[self.pos + 2].type in self.TYPE_TOKENS
        ):
            self.advance()  # contextual `c` declaration keyword
            return self.parse_declaration_after_kind("c")
        if token.type is TokenType.FN:
            return self.parse_function()
        if token.type in (TokenType.START, TokenType.PROCESS):
            return self.parse_named_function()
        if token.type is TokenType.IF:
            return self.parse_if()
        if token.type is TokenType.MAT:
            self.error(
                token,
                "`mat` is tokenized, but its case/branch syntax is not currently "
                "clearly defined in the specification"
            )
        if token.type is TokenType.RETURN:
            return self.parse_return()
        if token.type is TokenType.PASS:
            # `pass` at the start of a line skips the entire current line.
            # The tokenizer marks every line ending with a NEWLINE token,
            # so the parser consumes the complete line after `pass`.
            self.advance()
            while not self.at(TokenType.NEWLINE) and not self.at(TokenType.EOF):
                self.advance()
            self.match(TokenType.NEWLINE)
            return PassStmt()
        if token.type is TokenType.AWAIT:
            self.advance()
            expression = self.parse_expression()
            self.expect(TokenType.NEWLINE, "a line ending is required after `await`")
            return AwaitStmt(expression)

        if token.type is TokenType.PRINT_CMD:
            return self.parse_print_cmd()

        return self.parse_assignment_or_expression()

    def parse_include(self) -> Include:
        self.expect(TokenType.LT, "`<` is required before `include`")
        self.expect(TokenType.INCLUDE, "`include` is required inside `<...>`")
        self.expect(TokenType.GT, "`>` is required after `include`")

        modules: list[str] = []
        while True:
            module = self.expect(
                TokenType.IDENTIFIER,
                "a module name is required after `<include>`"
            )
            modules.append(module.value)

            if not self.match(TokenType.COMMA):
                break

        self.expect(TokenType.NEWLINE, "a line ending is required after `<include>`")
        return Include(modules)

    def parse_declaration(self) -> Declaration:
        kind = self.advance().value
        return self.parse_declaration_after_kind(kind)

    def parse_declaration_after_kind(self, kind: str) -> Declaration:
        name = self.expect(
            TokenType.IDENTIFIER,
            "the first name in a declaration must be an identifier"
        )

        type_token = self.current()
        if type_token.type not in self.TYPE_TOKENS:
            self.error(
                type_token,
                "a type name is required in a declaration"
            )
        type_name = self.TYPE_TOKENS[self.advance().type]

        value = None
        if self.match(TokenType.ASSIGN):
            if type_name == "FunctionalObject":
                value = self.parse_functional_object()
            else:
                value = self.parse_expression()

        if not (type_name == "FunctionalObject" and isinstance(value, FunctionalObjectDef)):
            self.expect(TokenType.NEWLINE, "a line ending is required at the end of a declaration")
        return Declaration(kind, name.value, type_name, value)

    def parse_functional_object(self) -> FunctionalObjectDef:
        name = self.current()
        if name.type is not TokenType.TYPE_FUNCTIONAL_OBJECT:
            self.error(name, "a FunctionalObject assignment must use `FunctionalObject.new(...)`")
        self.advance()
        self.expect(TokenType.DOT, "a dot is required after `FunctionalObject`")
        new_token = self.expect(TokenType.IDENTIFIER, "`new` is required after `FunctionalObject.`")
        if new_token.value != "new":
            self.error(new_token, "the FunctionalObject constructor must be named `new`")
        parameters = self.parse_parameter_list()
        self.expect(TokenType.COLON, "the FunctionalObject header must end with `:`")
        self.expect(TokenType.NEWLINE, "a line ending is required after `:`")
        body = self.parse_block()
        return FunctionalObjectDef(parameters, body)

    def parse_function(self) -> FunctionDef:
        self.advance()  # fn
        name = self.expect(TokenType.IDENTIFIER, "a function name is required after `fn`")
        parameters = self.parse_parameter_list()
        self.expect(TokenType.COLON, "the function header must end with `:`")
        self.expect(TokenType.NEWLINE, "a line ending is required after `:`")
        body = self.parse_block()
        return FunctionDef(name.value, parameters, body)

    def parse_named_function(self) -> FunctionDef:
        name_token = self.advance()
        parameters = self.parse_parameter_list()
        self.expect(TokenType.COLON, "the function header must end with `:`")
        self.expect(TokenType.NEWLINE, "a line ending is required after `:`")
        body = self.parse_block()
        return FunctionDef(name_token.value, parameters, body)

    def parse_parameter_list(self) -> list[str]:
        self.expect(TokenType.LPAREN, "`(` is required after the function name")
        parameters: list[str] = []

        if not self.at(TokenType.RPAREN):
            while True:
                param = self.expect(
                    TokenType.IDENTIFIER,
                    "a function parameter must be an identifier"
                )
                parameters.append(param.value)
                if not self.match(TokenType.COMMA):
                    break

        self.expect(TokenType.RPAREN, "missing `)` in the parameter list")
        return parameters

    def parse_block(self) -> list[object]:
        self.expect(TokenType.INDENT, "an indented line is required for the block")
        self.skip_newlines()

        statements = []
        while not self.at(TokenType.DEDENT) and not self.at(TokenType.EOF):
            statements.append(self.parse_statement())
            self.skip_newlines()

        self.expect(TokenType.DEDENT, "missing block terminator")
        return statements

    def parse_if(self) -> IfStmt:
        self.advance()  # if
        condition = self.parse_expression()
        self.expect(TokenType.COLON, "`if` must end with `:`")
        self.expect(TokenType.NEWLINE, "a line ending is required after `if`")
        body = self.parse_block()

        elif_blocks = []
        while self.match(TokenType.ELIF):
            elif_condition = self.parse_expression()
            self.expect(TokenType.COLON, "`elif` must end with `:`")
            self.expect(TokenType.NEWLINE, "a line ending is required after `elif`")
            elif_body = self.parse_block()
            elif_blocks.append((elif_condition, elif_body))

        else_body = None
        if self.match(TokenType.ELSE):
            self.expect(TokenType.COLON, "`else` must end with `:`")
            self.expect(TokenType.NEWLINE, "a line ending is required after `else`")
            else_body = self.parse_block()

        return IfStmt(condition, body, elif_blocks, else_body)

    def parse_print_cmd(self) -> PrintCmdStmt:
        self.advance()  # print_cmd
        self.expect(
            TokenType.LPAREN,
            "`(` is required after `print_cmd`"
        )
        expression = self.parse_expression()
        self.expect(
            TokenType.RPAREN,
            "missing `)` in the `print_cmd` call"
        )
        self.expect(
            TokenType.NEWLINE,
            "a line ending is required after `print_cmd`"
        )
        return PrintCmdStmt(expression)


    def parse_return(self) -> ReturnStmt:
        self.advance()
        if self.at(TokenType.NEWLINE):
            self.advance()
            return ReturnStmt(None)

        value = self.parse_expression()
        self.expect(TokenType.NEWLINE, "a line ending is required after `return`")
        return ReturnStmt(value)

    def parse_assignment_or_expression(self):
        expression = self.parse_expression()

        if isinstance(expression, Name) and self.current().type in self.ASSIGNMENT_TOKENS:
            operator = self.ASSIGNMENT_TOKENS[self.advance().type]
            value = self.parse_expression()
            self.expect(TokenType.NEWLINE, "a line ending is required after the assignment")
            return Assignment(expression.name, operator, value)

        self.expect(TokenType.NEWLINE, "a line ending is required after the expression")
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

        while True:
            if self.match(TokenType.LPAREN):
                arguments = []
                if not self.at(TokenType.RPAREN):
                    while True:
                        arguments.append(self.parse_expression())
                        if not self.match(TokenType.COMMA):
                            break
                self.expect(TokenType.RPAREN, "missing `)` in the call")
                expr = CallExpr(expr, arguments)
                continue

            if self.match(TokenType.DOT):
                method = self.expect(
                    TokenType.IDENTIFIER,
                    "a method name is required after `.`"
                )
                if method.value != "type":
                    self.error(method, "only `type()` is currently supported here")

                self.expect(
                    TokenType.LPAREN,
                    "`(` is required after `.type`"
                )

                target_types = {
                    TokenType.TYPE_INT: "int",
                    TokenType.TYPE_FLOAT: "float",
                    TokenType.TYPE_STRING: "string",
                    TokenType.TYPE_BOOL: "bool",
                }

                # type() with no argument queries the caller's current type.
                if self.match(TokenType.RPAREN):
                    expr = TypeConversionExpr(expr, None)
                    continue

                target = self.current()
                if target.type not in target_types:
                    self.error(
                        target,
                        "type() requires one of: int, float, string, bool"
                    )

                self.advance()
                target_type = target_types[target.type]

                if not self.at(TokenType.RPAREN):
                    self.error(
                        self.current(),
                        "type() receives only 1 argument"
                    )

                self.advance()
                expr = TypeConversionExpr(expr, target_type)
                continue

            return expr

    def parse_primary(self):
        token = self.current()

        if token.type is TokenType.LPAREN:
            self.advance()
            expression = self.parse_expression()
            self.expect(TokenType.RPAREN, "missing `)` in the parenthesized expression")
            return expression

        if token.type is TokenType.INTEGER:
            self.advance()
            return Literal(token.value)

        if token.type is TokenType.TRUE:
            self.advance()
            return Literal(True)

        if token.type is TokenType.FALSE:
            self.advance()
            return Literal(False)

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
                "a type name is not an expression here"
            )

        self.error(token, "a valid expression was expected")
        raise AssertionError("unreachable")


def ast_to_dict(node):
    """Small debug helper: convert the AST into an easily printable JSON-like dict."""
    if is_dataclass(node):
        result = {}
        for key, value in asdict(node).items():
            result[key] = value
        return result
    return node
