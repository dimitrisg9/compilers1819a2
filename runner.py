import plex


class ParseError(Exception):
    pass


class ParseRun(Exception):
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
        self.st = {}
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
            varname = self.text
            self.match('IDENTIFIER')
            self.match('=')
            e = self.expr()
            self.st[varname] = e
        elif self.la == 'PRINT':
            self.match('PRINT')
            e = self.expr()
            print('{:b}'.format(e))
        else:
            raise ParseError("perimenw IDENTIFIER or PRINT")

    def expr(self):
        if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'BIT_TOKEN':
            t = self.term()
            while self.la == 'XOR':
                self.match("XOR")
                t2 = self.term()
                t ^= t2
            if self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
                return t
            else:
                raise ParseError("perimenw XOR")
        else:
            raise ParseError("perimenw ( or IDENTIFIER or BIT or )")

    def term(self):
        if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'BIT_TOKEN':
            t = self.factor()
            while self.la == 'OR':
                self.match('OR')
                t2 = self.factor()
                t |= t2

            if self.la == 'XOR' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
                return t
            else:
                print(self.la)
                raise ParseError("perimenw ( or IDENTIFIER or BIT or )")
        else:
            raise ParseError("perimenw * or /")

    def factor(self):
        if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'BIT_TOKEN':
            t = self.atom()
            while self.la == 'AND':
                self.match('AND')
                t2 = self.atom()
                t &= t2

            if self.la == 'XOR' or self.la == 'OR' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
                return t
            else:
                print(self.la)
                raise ParseError("perimenw ( or IDENTIFIER or BIT or )")
        else:
            raise ParseError("perimenw AND or /")

    def atom(self):
        if self.la == '(':
            self.match('(')
            e = self.expr()
            self.match(')')
            return e
        elif self.la == 'IDENTIFIER':
            varname = self.text
            self.match('IDENTIFIER')
            if varname in self.st:
                return self.st[varname]
            raise ParseRun("perimenw id poy exei arxikopoih8h")
        elif self.la == 'BIT_TOKEN':
            value = int(self.text, 2)
            self.match('BIT_TOKEN')
            return value
        else:
            raise ParseError("perimenw id float or (")




parser = MyParser()
with open('test.txt', 'r') as fp:
    parser.parse(fp)


