from __future__ import annotations
from ..lexer import Lexer, Reader, Keywords, Token
from .._Env import Env
from .nodes import Program


class Parser:
    lex: Lexer
    top: Env
    look: Token | Keywords

    block_num = 0

    def __init__(self, lex: Lexer):
        self.lex = lex
        self.top = None

    @staticmethod
    def from_file(file_path: str) -> Parser:
        reader = Reader.from_file(file_path)
        lexer = Lexer(reader)
        return Parser(lexer)

    def move(self):
        try:
            self.look = next(self.token_generator)
        except StopIteration:
            self.look = None

    def match(self, tag: Keywords | Token):
        if self.look.value == tag.value:
            self.move()
        else:
            self.lex.error(f"Expected {tag}, found {self.look}")

    def gen(self):
        self.token_generator = self.lex.tokens()
        self.move()
        Program(self).gen()
