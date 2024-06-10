class Token:
    EOF = "<EOF>" #-1
    EOF_TYPE = 1
    PLUSZ = 2
    MINUSZ = 3
    SZORZAS = 4
    OSZTAS = 5
    BAL_ZAROJEL = 6
    JOBB_ZAROJEL = 7
    SZAM = 8
    HATVANY = 9
    FUGGVENY = 10
    KAPCSOS_BAL = 11
    KAPCSOS_JOBB = 12

    token_names = ["n/a", "<EOF>", "PLUSZ", "MINUSZ", "SZORZAS", "OSZTAS", "BAL_ZAROJEL", "JOBB_ZAROJEL", "SZAM", "HATVANY", "FUGGVENY", "KAPCSOS ZAROJEL, BAL", "KAPCSOS ZAROJEL, JOBB"]
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        tname = Token.token_names[self.type]
        return f"<'{self.value}', {tname}>"

    def __repr__(self):
        return self.__str__()

class Lexer:
    DIGITS = '0123456789'
    FUNCTIONS = ["log", "sqrt", "cos", "sin", "tg", "abs", "ctg"]
    def __init__(self, input):
        self.input = input
        self.p = 0  # pozicio
        self.c = self.input[self.p]  # jelenlegi karakter

    def consume(self):
        self.p += 1
        if self.p >= len(self.input):
            self.c = Token.EOF
        else:
            self.c = self.input[self.p]

    def whitespace(self):
        while self.c in [' ', '\t', '\n', '\r']:
            self.consume()

    def match(self, x):
        if self.c == x:
            self.consume()
        else:
            raise Exception(f"Expected {x}; found {self.c}")

    def next_token(self):
        while self.c != Token.EOF:
            if self.c in [' ', '\t', '\n', '\r']:
                self.whitespace()
                continue
            elif self.c == '+':
                self.consume()
                return Token(Token.PLUSZ, "+")
            elif self.c == '-':
                self.consume()
                return Token(Token.MINUSZ, "-")
            elif self.c == '*':
                self.consume()
                return Token(Token.SZORZAS, "*")
            elif self.c == '/':
                self.consume()
                return Token(Token.OSZTAS, "/")
            elif self.c == '(':
                self.consume()
                return Token(Token.BAL_ZAROJEL, "(")
            elif self.c == ')':
                self.consume()
                return Token(Token.JOBB_ZAROJEL, ")")
            elif self.c == '{':
                self.consume()
                return Token(Token.KAPCSOS_BAL, "{")
            elif self.c == '}':
                self.consume()
                return Token(Token.KAPCSOS_JOBB, "}")
            elif self.c == '^':
                self.consume()
                return Token(Token.HATVANY, "^")
            elif self.c in Lexer.DIGITS or self.c == '.':
                db = 0
                szam = ''
                while ((self.c in Lexer.DIGITS or (self.c == '.' and db <= 1)) and self.c != Token.EOF):
                    szam += self.c
                    if self.c == '.':
                        db += 1
                    self.consume()
                return Token(Token.SZAM, szam)
            elif self.c.isalpha():
                fuggv = ''
                while (self.c.isalpha()):
                    fuggv += self.c
                    self.consume()
                if fuggv in Lexer.FUNCTIONS:
                    return Token(Token.FUGGVENY, fuggv)
            else:
                raise Exception(f"Invalid karakter: {self.c}")
        return Token(Token.EOF_TYPE, "<EOF>")
