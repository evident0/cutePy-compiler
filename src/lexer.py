from enum import Enum
DIGITS = '0123456789'
LETTERS = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'


class Family(Enum):
    EOF = 0
    NUMBER = 1
    ADDOP = 2
    MULOP = 3
    IDENTIFIER = 4
    KEYWORD = 5
    GROUPSYMBOL = 6
    DELIMITER = 7
    DECLARATION = 8
    RELOP = 9
    ASSIGNMENT = 10


class Token:
    def __init__(self, family, recognized_string, line_number):
        self.family = family
        self.recognized_string = recognized_string
        self.line_number = line_number

    def __repr__(self):
        return f'[{self.family} | {self.recognized_string} | line number: {self.line_number}]'


class Lexer:
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.position = -1
        self.line_number = 1
        self.current_char = None
        self.next_char()

    def next_char(self):
        self.position += 1
        if self.current_char == '\n':
            self.line_number += 1
        self.current_char = self.raw_text[self.position] if self.position < len(self.raw_text) else None

    def next_token(self):
        token = None
        if self.current_char is None:
            return Token(Family.EOF, "EOF", self.line_number)

        while self.current_char in '\t \n':
            self.next_char()
            if self.current_char is None:
                return Token(Family.EOF, "EOF", self.line_number)

        if self.current_char in DIGITS:
            token = (self.make_dig())
        elif self.current_char in LETTERS:
            token = (self.make_idk())
        elif self.current_char == '_':
            token = self.make_name()
        elif self.current_char == '\"':
            token = self.make_main()
        elif self.current_char in '+-':
            token = (Token(Family.ADDOP, self.current_char, self.line_number))
            self.next_char()
        elif self.current_char == '*':
            token = (Token(Family.MULOP, self.current_char, self.line_number))
            self.next_char()
        elif self.current_char == '/':
            token = (self.make_div())
        elif self.current_char == '#':
            token = self.make_hashtag()
        elif self.current_char in '()[]':
            token = (Token(Family.GROUPSYMBOL, self.current_char, self.line_number))
            self.next_char()
        elif self.current_char in ',;:':
            token = (Token(Family.DELIMITER, self.current_char, self.line_number))
            self.next_char()
        elif self.current_char == '=':
            token = (self.make_asgn())
        elif self.current_char in '<>':
            token = (self.make_smlg())
        elif self.current_char == '!':
            token = (self.make_different())
        else:
            exit(f"LexError in Line: {self.line_number}: Unknown Symbol")
        return token

    def make_dig(self):
        num_str = ''
        while self.current_char is not None and self.current_char in DIGITS:
            num_str += self.current_char
            self.next_char()
        if self.current_char in LETTERS:
            exit(f"LexError in Line: {self.line_number}: Expected digit but found character")
        return Token(Family.NUMBER, num_str, self.line_number)

    def make_idk(self):
        idk_str = ''
        while self.current_char is not None and self.current_char in DIGITS or self.current_char in LETTERS+'_':
            idk_str += self.current_char
            self.next_char()
        if idk_str in ["and", "or", "not"]:
            return Token(Family.RELOP, idk_str, self.line_number)
        if idk_str in ["if", "else", "while", "return", "def"]:
            return Token(Family.KEYWORD, idk_str, self.line_number)
        return Token(Family.IDENTIFIER, idk_str, self.line_number)

    def make_name(self):
        self.next_char()
        for i in '_name__':
            if self.current_char == i:
                self.next_char()
            else:
                exit(f"LexError in Line: {self.line_number}: Expected __name__")

        return Token(Family.KEYWORD, '__name__', self.line_number)

    def make_main(self):
        self.next_char()
        for i in '__main__\"':
            if self.current_char == i:
                self.next_char()
            else:
                exit(f"LexError in Line: {self.line_number}: Expected \"__main__\"")

        return Token(Family.KEYWORD, '\"__main__\"', self.line_number)

    def make_div(self):
        div_str = self.current_char
        self.next_char()
        if self.current_char == "/":
            div_str += self.current_char
            self.next_char()
            return Token(Family.MULOP, div_str, self.line_number)
        else:
            exit(f"LexError in Line: {self.line_number}: Expected //")

    def make_hashtag(self):
        hashtag_str = self.current_char
        self.next_char()
        if self.current_char in '{}':
            hashtag_str += self.current_char
            self.next_char()
            return Token(Family.MULOP, hashtag_str, self.line_number)
        elif self.current_char in LETTERS:
            while self.current_char in LETTERS:
                hashtag_str += self.current_char
                self.next_char()
            if hashtag_str == '#declare':
                return Token(Family.DECLARATION, hashtag_str, self.line_number)
            exit(f"LexError in Line: {self.line_number}: Expected #declare")
        elif self.current_char == '$':
            while True:
                if self.current_char == "#":
                    self.next_char()
                    if self.current_char == "$":
                        self.next_char()
                        break
                if self.current_char is None:
                    exit(f"LexError in Line: {self.line_number}: Found EOF in comment")
                self.next_char()
            return self.next_token()

        else:
            exit(f"LexError in Line: {self.line_number}: Unexpected character after #")

    def make_asgn(self):
        asgn_str = self.current_char
        self.next_char()
        if self.current_char == '=':
            asgn_str += self.current_char
            self.next_char()
            return Token(Family.RELOP, asgn_str, self.line_number)
        else:
            return Token(Family.ASSIGNMENT, asgn_str, self.line_number)

    def make_smlg(self):
        smgl_str = self.current_char
        self.next_char()
        if self.current_char == '=':
            smgl_str += self.current_char
            self.next_char()
            return Token(Family.RELOP, smgl_str, self.line_number)
        else:
            return Token(Family.RELOP, smgl_str, self.line_number)

    def make_different(self):
        different_str = self.current_char
        self.next_char()
        if self.current_char == '=':
            different_str += self.current_char
            self.next_char()
            return Token(Family.RELOP, different_str, self.line_number)
        else:
            exit(f"LexError in Line: {self.line_number}: Expected !=")

