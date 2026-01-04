class LexerException(Exception):
    def __init__(self, message, file, line, column):
        self.message = message
        self.file = file
        self.line = line
        self.column = column
        super().__init__(message)

    def __str__(self):
        return f"{self.message} at File \"{self.file}\", line {self.line}, col {self.column}"