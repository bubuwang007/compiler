from src import Lexer, Reader

l = Lexer(Reader.from_file("test.st"))

for i in l.tokens():
    print(i)