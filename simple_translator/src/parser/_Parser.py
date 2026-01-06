from __future__ import annotations
from ..lexer import Lexer, Reader, Keywords, Token
from .._Env import Env
from .nodes import Program

class Parser:
    lex: Lexer
    top: Env
    look: Token | Keywords

    def __init__(self, lex: Lexer):
        self.lex = lex

    @staticmethod
    def from_file(file_path: str) -> Parser:
        reader = Reader.from_file(file_path)
        lexer = Lexer(reader)
        return Parser(lexer)

    def move(self):
        self.look = next(self.token_generator)

    def match(self, tag: Keywords | Token):
        if self.look.value == tag.value:
            self.move()
        else:
            self.lex.error(f"Expected {tag}, found {self.look}")

    def gen(self):
        self.token_generator = self.lex.tokens()
        Program(self).gen()
