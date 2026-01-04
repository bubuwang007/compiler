from __future__ import annotations


class Reader:
    _content: str
    file: str
    current: int
    line: int
    column: int

    def __init__(self, content: str, file: str):
        self._content = content
        self.file = file

    @staticmethod
    def from_file(file_path: str) -> Reader:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return Reader(content, file_path)

    @staticmethod
    def from_string(content: str) -> Reader:
        return Reader(content, "<string>")

    def init(self) -> None:
        self.current = 0
        self.line = 1
        self.column = 1

    def next_char(self, n: int = 1) -> str | None:
        if self.current + n > len(self._content):
            return None
        return self._content[self.current + n - 1]

    def consume_char(self, n: int = 1, newline: bool = False):
        if newline:
            self.current += n
            self.line += 1
            self.column = 1
        else:
            self.current += n
            self.column += n
