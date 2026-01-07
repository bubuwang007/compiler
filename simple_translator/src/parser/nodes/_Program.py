from ._Node import Node
from ._Block import Block

class Program(Node):

    def gen(self):
        print("Program Start")
        block = Block(self.parser)
        block.gen()
        print("Program End")