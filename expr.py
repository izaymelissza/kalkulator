from lexer import Lexer
from lexer import Token
from parser import Parser
import math

class Expr:
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self):
        lexer = Lexer(self.expression)
        try:
            parser = Parser(lexer)
            result = self._kiertekel(parser.root)
            print(result)
        except Exception as inst:
            print(inst)

    def _kiertekel(self, cs):
        left = right = None
        if cs.left is not None:
            left = self._kiertekel(cs.left)
        if cs.right is not None:
            right = self._kiertekel(cs.right)

        if cs.token.type == Token.SZAM:
            return float(cs.token.value)
        elif cs.token.type == Token.PLUSZ:
            return left + right
        elif cs.token.type == Token.MINUSZ:
            return left - right
        elif cs.token.type == Token.SZORZAS:
            return left * right
        elif cs.token.type == Token.OSZTAS:
            return left / right
        elif cs.token.type == Token.HATVANY:
            return left ** right
        elif cs.token.type == Token.HATVANY:
            return left ** right
        elif cs.token.type == Token.FUGGVENY:
            if cs.token.value == "log":
                return math.log(left, right)
            elif cs.token.value == "sqrt":
                return math.sqrt(left)
            elif cs.token.value == "abs":
                return abs(left)
            elif cs.token.value == "sin":
                return math.sin(left * (math.pi / 180))
            elif cs.token.value == "cos":
                return math.cos(left * (math.pi / 180))
            elif cs.token.value == "tg":
                return math.tan(left * (math.pi / 180))
            elif cs.token.value == "ctg":
                return 1 / (math.tan(left * (math.pi / 180)))

