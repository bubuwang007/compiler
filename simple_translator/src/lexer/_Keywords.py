from __future__ import annotations
import enum


class Keywords(enum.Enum):
    mapping: dict

    TRUE = "true"
    FALSE = "false"

    DO = "do"
    WHILE = "while"
    IF = "if"
    ELSE = "else"
    BREAK = "break"

    @staticmethod
    def get(value: str) -> Keywords | None:
        return Keywords.mapping.get(value, None)


Keywords.mapping = {kw.value: kw for kw in Keywords}
