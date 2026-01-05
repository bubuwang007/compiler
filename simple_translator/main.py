from src import Lexer, Reader

l = Lexer(Reader.from_file("code.st"))

with open("tokens.txt", "w", encoding="utf-8") as f:
    for i in l.tokens():
        print(i, file=f)
