import plex


class ParseError(Exception):
    pass


class MyParser:
    def __init__(self):
        dong = plex.Str('(', ')')
        letter = plex.Range('azAZ')
        digit = plex.Range('09')
        digit1 = plex.Range('01')
        bit = plex.Rep1(digit1)
        name = letter + plex.Rep(letter | digit)
        keyword = plex.Str('print', 'PRINT')
        space = plex.Any(" \n\t")
        operator = plex.Str('XOR', 'AND', 'OR', '=')
        self.lexicon = plex.Lexicon([
            (operator, plex.TEXT),
            (bit, 'BIT_TOKEN'),
            (keyword, 'PRINT'),
            (dong, plex.TEXT),
            (name, 'IDENTIFIER'),
            (space, plex.IGNORE),
        ])

    def create_scanner(self, fp):
        self.scanner = plex.Scanner(self.lexicon, fp)
        self.la, self.text = self.next_token()

    def next_token(self):
        return self.scanner.read()

    def match(self, token):
        if self.la == token:
            self.la, self.text = self.next_token()
        else:
            raise ParseError("perimenw ! ? (")

    def parse(self, fp):
        self.create_scanner(fp)
        self.stmt_list()

    def stmt_list(self):
        if self.la == 'IDENTIFIER' or self.la == 'PRINT':
            self.stmt()
            self.stmt_list()
        elif self.la == None:
            return
        else:
            raise ParseError("perimenw IDENTIFIER or Print")

    def stmt(self):
        if self.la == 'IDENTIFIER':
            self.match('IDENTIFIER')
            self.match('=')
            self.expr()
        elif self.la == 'PRINT':
            self.match('PRINT')
            self.expr()
        else:
            raise ParseError("perimenw IDENTIFIER or PRINT")

    def expr(self):
        if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'BIT_TOKEN':
            self.term()
            self.term_tail()
        else:
            raise ParseError("perimenw ( or IDENTIFIER or BIT or )")

    def term_tail(self):
        if self.la == 'XOR':
            self.match('XOR')
            self.term()
            self.term_tail()
        elif self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
            return
        else:
            raise ParseError("perimenw XOR ")

    def term(self):
        if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'BIT_TOKEN' or self.la == ')':
            self.factor()
            self.factor_tail()
        else:
            raise ParseError("perimenw ( or IDENTIFIER or BIT or )")

    def factor_tail(self):
        if self.la == 'OR':
            self.match('OR')
            self.factor()
            self.factor_tail()
        elif self.la == 'XOR' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
            return
        else:
            raise ParseError("perimenw OR or /")

    def factor(self):
        if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'BIT_TOKEN' or self.la == ')':
            self.atom()
            self.atom_tail()
        else:
            raise ParseError("perimenw id bit or (")

    def atom_tail(self):
        if self.la == 'AND':
            self.match('AND')
            self.atom()
            self.atom_tail()
        elif self.la == 'OR' or self.la=='XOR' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
            return
        else:
            raise ParseError("perimenw AND or /")

    def atom(self):
        if self.la == '(':
            self.match('(')
            self.expr()
            self.match(')')
        elif self.la == 'IDENTIFIER':
            self.match('IDENTIFIER')
        elif self.la == 'BIT_TOKEN':
            self.match('BIT_TOKEN')
        else:
            raise ParseError("perimenw id bit or (")


parser = MyParser()
with open('test.txt', 'r') as fp:
    parser.parse(fp)

