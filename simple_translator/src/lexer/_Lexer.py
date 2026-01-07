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
            elif c == "'":
                yield self.char()
                continue
            elif c == '"':
                yield self.string()
                continue
            elif self.is_potential_identifier_start(c):
                yield self.identifier_or_keywords()
                continue
            elif c.isdigit():
                yield self.number()
                continue
            elif (tok := self.symbol(c)) is not None:
                yield tok
                continue
            raise self.error("Invalid character")

    def error(self, message):
        raise LexerException(
            message,
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

    def char(self) -> TokenInfo:
        self._reader.consume_char()
        c = self._reader.next_char()
        if c is None:
            self.error("Unterminated character literal")
        self._reader.consume_char()
        if self._reader.next_char() != "'":
            self.error("Only one character allowed in character literal")
        self._reader.consume_char()
        return TokenInfo(
            Token.CHAR,
            self._reader._content[self.start : self._reader.current],
            self._reader.line,
            self.start_column,
            self._reader.column - 1,
        )

    def string(self) -> TokenInfo:
        self._reader.consume_char()
        s = []
        while True:
            c = self._reader.next_char()

            if c is None or c == "\n":
                self.error("Unterminated string literal")
            elif c == "\\":
                self._reader.consume_char()
                t = self._reader.next_char()
                match t:
                    case "n":
                        s.append("\n")
                    case "t":
                        s.append("\t")
                    case "\\":
                        s.append("\\")
                    case '"':
                        s.append('\"')
                    case "0":
                        s.append("\0")
                    case "r":
                        s.append("\r")
                    case "b":
                        s.append("\b")
                    case "f":
                        s.append("\f")
                    case "v":
                        s.append("\v")
                    case "a":
                        s.append("\a")
                    case _:
                        self.error("Invalid escape sequence")
            elif c == '"':
                self._reader.consume_char()
                return TokenInfo(
                    Token.STR,
                    self._reader._content[self.start : self._reader.current],
                    self._reader.line,
                    self.start_column,
                    self._reader.column - 1,
                )
            elif c is None:
                self.error("Unterminated string literal")
            else:
                s.append(c)
            self._reader.consume_char()

    def identifier_or_keywords(self) -> TokenInfo:

        while True:
            c = self._reader.next_char()

            if c is None or not self.is_potential_identifier(c):
                tok = self._reader._content[self.start : self._reader.current]

                if (kw := Keywords.get(tok)) is not None:
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
            elif c == "e" or c == "E":
                self._reader.consume_char()
                return self.scientific()
            elif c is None or not c.isdigit():
                return TokenInfo(
                    Token.INT,
                    self._reader._content[self.start : self._reader.current],
                    self._reader.line,
                    self.start_column,
                    self._reader.column - 1,
                )
            elif c.isdigit():
                self._reader.consume_char()

    def float(self) -> TokenInfo:
        while True:
            c = self._reader.next_char()
            if c == "e" or c == "E":
                self._reader.consume_char()
                return self.scientific()
            elif c is None or not c.isdigit():
                return TokenInfo(
                    Token.FLOAT,
                    self._reader._content[self.start : self._reader.current],
                    self._reader.line,
                    self.start_column,
                    self._reader.column - 1,
                )
            elif c.isdigit():
                self._reader.consume_char()

    def scientific(self) -> TokenInfo:
        c = self._reader.next_char()
        if c == "+" or c == "-":
            self._reader.consume_char()

        while True:
            c = self._reader.next_char()
            if c is None or not c.isdigit():
                return TokenInfo(
                    Token.FLOAT,
                    self._reader._content[self.start : self._reader.current],
                    self._reader.line,
                    self.start_column,
                    self._reader.column - 1,
                )
            elif c.isdigit():
                self._reader.consume_char()

    def symbol(self, c: str) -> TokenInfo:
        return self.two_char_symbol(c)

    def two_char_symbol(self, c1: str) -> TokenInfo:
        c2 = self._reader.next_char(2)
        tok = Token.get_two_char(c1, c2)

        if tok is not None:
            self._reader.consume_char(2)
            return TokenInfo(
                tok,
                self._reader._content[self.start : self._reader.current],
                self._reader.line,
                self.start_column,
                self._reader.column - 1,
            )
        else:
            return self.one_char_symbol(c1)

    def one_char_symbol(self, c1: str) -> TokenInfo:
        tok = Token.get_one_char(c1)

        if tok is not None:
            self._reader.consume_char()
            return TokenInfo(
                tok,
                self._reader._content[self.start : self._reader.current],
                self._reader.line,
                self.start_column,
                self._reader.column - 1,
            )
