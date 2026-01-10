from ...symbols._Env import Env
from ._Node import Node
from ...lexer import Token
from ._Decls import Decls

class Block(Node):

    def gen(self):
        self.parser.block_num += 1
        print(f"Block {self.parser.block_num} Start")
        self.parser.match(Token.LBRACE)
        saved_env = self.parser.top
        self.parser.top = Env(saved_env)

        Decls(self.parser).gen()

        self.parser.match(Token.RBRACE)
        self.parser.top = saved_env
        print(f"Block {self.parser.block_num} End")
