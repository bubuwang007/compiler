import dataclasses
from ._Token import Token
from ._Keywords import Keywords


@dataclasses.dataclass
class TokenInfo:
    token: Token | Keywords
    value: str
    line: int
    start_column: int
    end_column: int

    def __str__(self) -> str:
        return f"{self.token}, {self.value!r}, line:{self.line}, sc:{self.start_column}, ec:{self.end_column}"
