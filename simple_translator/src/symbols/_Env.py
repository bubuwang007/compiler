from __future__ import annotations


class Env:
    prev: Env | None
    table: dict[str, object]

    def __init__(self, prev: Env | None = None) -> None:
        self.prev = prev
        self.table = {}

    def get(self, name: str) -> object | None:
        e: Env | None = self
        while e is not None:
            v = e.table.get(name)
            if v is not None:
                return v
            e = e.prev
        return None

    def put(self, name: str, value: object) -> None:
        self.table[name] = value
