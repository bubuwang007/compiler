from ._Node import Node
from ...lexer import Token


class Decls(Node):

    def gen(self):
        print("Declarations Start")

        while Token.is_basic_type(self.parser.look):
            pass

        print("Declarations End")
