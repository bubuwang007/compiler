from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .._Parser import Parser

class Program:

    parser: Parser

    def __init__(self, parser: Parser):
        self.parser = parser

    def gen(self):
        print("Program")