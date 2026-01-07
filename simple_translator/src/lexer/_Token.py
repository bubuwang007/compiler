from __future__ import annotations
import enum


class Token(enum.Enum):
    ONECHAR: dict[str, Token]
    TWOCHAR: dict[str, dict[str, Token]]

    INT = "int"
    FLOAT = "float"
    CHAR = "char"
    STR = "str"

    KEYWORD = "keyword"
    IDENTIFIER = "id"
    COMMENT = "comment"

    SEMICOLON = ";"
    LBRACE = "{"
    RBRACE = "}"
    LPAR = "("
    RPAR = ")"
    LSQB = "["
    RSQB = "]"

    EQ = "="
    EQEQ = "=="
    NE = "!="
    NOT = "!"

    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"

    AMPER = "&"
    VBAR = "|"
    DOUBLEAMPER = "&&"
    DOUBLEVBAR = "||"

    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="

    def __str__(self) -> str:
        return "Token." + self.name

    @staticmethod
    def get_two_char(c1, c2):
        return Token.TWOCHAR.get(c1, {}).get(c2)

    @staticmethod
    def get_one_char(c):
        return Token.ONECHAR.get(c)

    @staticmethod
    def is_basic_type(token: Token) -> bool:
        return token in [Token.INT, Token.FLOAT, Token.CHAR, Token.STR]

Token.ONECHAR = {
    Token.SEMICOLON.value: Token.SEMICOLON,
    Token.LBRACE.value: Token.LBRACE,
    Token.RBRACE.value: Token.RBRACE,
    Token.LPAR.value: Token.LPAR,
    Token.RPAR.value: Token.RPAR,
    Token.LSQB.value: Token.LSQB,
    Token.RSQB.value: Token.RSQB,
    Token.EQ.value: Token.EQ,
    Token.PLUS.value: Token.PLUS,
    Token.MINUS.value: Token.MINUS,
    Token.STAR.value: Token.STAR,
    Token.SLASH.value: Token.SLASH,
    Token.LT.value: Token.LT,
    Token.GT.value: Token.GT,
    Token.NOT.value: Token.NOT,
}

Token.TWOCHAR = {
    Token.NOT.value: {Token.EQ.value: Token.NE},
    Token.EQ.value: {Token.EQ.value: Token.EQEQ},
    Token.LT.value: {Token.EQ.value: Token.LE},
    Token.GT.value: {Token.EQ.value: Token.GE},
    Token.AMPER.value: {Token.AMPER.value: Token.DOUBLEAMPER},
    Token.VBAR.value: {Token.VBAR.value: Token.DOUBLEVBAR},
}
