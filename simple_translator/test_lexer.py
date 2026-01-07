from src import Reader, Lexer

lex = Lexer(Reader.from_file("test.st"))

for token in lex.tokens():
    print(token.value)