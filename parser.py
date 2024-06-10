from lexer import Token

class Node:
    def __init__(self, token):
        self.token = token
        self.left = None
        self.right = None

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.currentToken = lexer.next_token()

        self.root = self.parse()

    def consume(self, token_type):
        if (self.currentToken.type == token_type):
            self.currentToken = self.lexer.next_token()
        else:
            raise Exception("Varatlan token: ", self.currentToken, Token.token_names[token_type])

    def parse(self):
        return self.sum()

    def sum(self):
        node = self.mul()
        while (self.currentToken.type == Token.PLUSZ or self.currentToken.type == Token.MINUSZ):
            left = node
            node = Node(self.currentToken)
            if (self.currentToken.type == Token.PLUSZ):
                self.consume(Token.PLUSZ)
            else:
                self.consume(Token.MINUSZ)
            right = self.mul()

            node.left = left
            node.right = right

        return  node

    def mul(self):
        node = self.power()
        while (self.currentToken.type == Token.SZORZAS or self.currentToken.type == Token.OSZTAS):
            left = node
            node = Node(self.currentToken)
            if (self.currentToken.type == Token.SZORZAS):
                self.consume(Token.SZORZAS)
            else:
                self.consume(Token.OSZTAS)
            right = self.power()

            node.left = left
            node.right = right

        return  node

    def power(self):
        node = self.faktor()
        while (self.currentToken.type == Token.HATVANY):
            left = node
            node = Node(self.currentToken)
            self.consume(Token.HATVANY)
            right = self.faktor()
            while (self.currentToken.type == Token.HATVANY):
                op = self.currentToken
                self.consume(Token.HATVANY)
                right = self.power()
            node.left = left
            node.right = right
        return node

    def faktor(self):
        node = None
        if (self.currentToken.type == Token.BAL_ZAROJEL):
            self.consume(Token.BAL_ZAROJEL)
            node = self.sum()
            self.consume(Token.JOBB_ZAROJEL)
        elif self.currentToken.type == Token.PLUSZ:
            node = Node(self.currentToken)
            self.consume(Token.PLUSZ)
            node.left = Node(Token(Token.SZAM, "0"))
            node.right = self.faktor()
        elif self.currentToken.type == Token.MINUSZ:
            node = Node(self.currentToken)
            self.consume(Token.MINUSZ)
            node.left = Node(Token(Token.SZAM, "0"))
            node.right = self.faktor()
        elif self.currentToken.type == Token.FUGGVENY:
            if self.currentToken.value == "log":
                node = Node(self.currentToken)
                self.consume(Token.FUGGVENY)
                self.consume(Token.KAPCSOS_BAL)
                right = self.sum()
                self.consume(Token.KAPCSOS_JOBB)
                self.consume(Token.BAL_ZAROJEL)
                left = self.sum()
                self.consume(Token.JOBB_ZAROJEL)
                node.left = left
                node.right = right
            else:
                node = Node(self.currentToken)
                self.consume(Token.FUGGVENY)
                self.consume(Token.BAL_ZAROJEL)
                left = self.sum()
                self.consume(Token.JOBB_ZAROJEL)
                node.left = left
        else:
            node = Node(self.currentToken)
            self.consume(Token.SZAM)
        return node
