from typing import Generator
from ._Reader import Reader
from ._TokenInfo import TokenInfo
from ._Token import Token
from ._Keywords import Keywords
from ._LexerException import LexerException


class Lexer:
    _reader: Reader

    def __init__(self, reader: Reader):
        self._reader = reader

    def is_potential_identifier_start(self, char: str) -> bool:
        return char.isalpha() or char == "_"

    def is_potential_identifier(self, char: str) -> bool:
        return char.isalnum() or char == "_"

    def tokens(self) -> Generator[TokenInfo, None, None]:
        self._reader.init()

        while True:
            c = self._reader.next_char()
            if c is None:
                break

            self.start = self._reader.current
            self.start_column = self._reader.column

            if c in [" ", "\t"]:
                self._reader.consume_char()
                continue
            elif c == "\n":
                self._reader.consume_char(newline=True)
                continue
            elif c == "#":
                yield self.comment()
                continue
            elif self.is_potential_identifier_start(c):
                yield self.identifier_or_keywords()
                continue
            elif c.isdigit():
                yield self.number()
                continue

            raise LexerException(
                "Invalid character",
                self._reader.file,
                self._reader.line,
                self.start_column,
            )

    def comment(self) -> TokenInfo:
        self._reader.consume_char()
        while True:
            c = self._reader.next_char()
            if c is None or c == "\n":
                return TokenInfo(
                    Token.COMMENT,
                    self._reader._content[self.start : self._reader.current],
                    self._reader.line,
                    self.start_column,
                    self._reader.column - 1,
                )
            self._reader.consume_char()

    def identifier_or_keywords(self) -> TokenInfo:

        while True:
            c = self._reader.next_char()

            if c is None or not self.is_potential_identifier(c):
                tok = self._reader._content[self.start : self._reader.current]

                if kw := Keywords.get(tok) is not None:
                    return TokenInfo(
                        kw,
                        tok,
                        self._reader.line,
                        self.start_column,
                        self._reader.column - 1,
                    )
                else:
                    return TokenInfo(
                        Token.IDENTIFIER,
                        tok,
                        self._reader.line,
                        self.start_column,
                        self._reader.column - 1,
                    )
            self._reader.consume_char()

    def number(self) -> TokenInfo:
        return self.int()

    def int(self) -> TokenInfo:

        while True:
            c = self._reader.next_char()
            if c == ".":
                self._reader.consume_char()
            return self.float()

    def float(self) -> TokenInfo:
        while True:
            c = self._reader.next_char()
            if c == "e" or c == "E":
                self._reader.consume_char()
