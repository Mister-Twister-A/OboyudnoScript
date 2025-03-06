from Token import Token, TokenType, lookup_ident
from typing import Any


class Lexer():
    def __init__(self, source: str):
        self.source = source

        self.position = -1
        self.read_position = 0
        self.line_no = 1
        self.cur_char : str | None = None

        self.__read_char()

    def __read_char(self):
        if self.read_position >= len(self.source):
            self.cur_char = None
        else: 
            self.cur_char = self.source[self.read_position]

        self.position = self.read_position
        self.read_position += 1

    def __next_char(self, len_):
        if self.read_position + (len_ - 1) >= len(self.source):
            return None
        else: 
            return self.source[self.read_position + (len_ - 1)]

    def __read_whitespace(self):
        while self.cur_char in [' ', '\t', '\r', '\n']:
            if self.cur_char == '\n':
                self.line_no +=1
            self.__read_char()

    def __new_token(self, type_: TokenType, literal: Any):
        return Token(type_,literal,self.line_no, self.position)
    
    def __is_digit(self, ch: str):
        return '0' <= ch and ch <= '9'
    def __is_letter(self, ch):
        return 'a' <= ch and ch <= 'z' or 'A' <= ch and ch <= 'Z' or ch == '_'
    
    def __read_number(self):
        start_pos : int = self.position
        num_dots : int = 0

        number : str = ""
        while self.__is_digit(self.cur_char) or self.cur_char == '.':
            if self.cur_char == '.':
                num_dots+=1

            if num_dots > 1:
                print(f"That shit is NOT a number at line {self.line_no} place {self.position}")
                return self.__new_token(TokenType.UNKNOWN, self.source[start_pos:self.position])
            
            number+=self.cur_char
            self.__read_char()

            if self.cur_char is None:
                break

        if num_dots == 0:
            return self.__new_token(TokenType.INT, int(number))
        else: 
            return self.__new_token(TokenType.FLOAT, float(number))
        
    def __read_indentifier(self):
        position = self.position
        # handle arrow
        if self.cur_char == 'B' and self.__next_char(1) == '-' and self.__next_char(2) == '-':
            self.__read_char()
            self.__read_char()
            self.__read_char()
            self.__read_char()
            return self.source[position:self.position]

        while self.cur_char is not None and (self.__is_letter(self.cur_char) or self.cur_char.isalnum()):
            self.__read_char()
        return self.source[position:self.position]
    
    def __read_str(self):
        position = self.position + 1
        while True:
            self.__read_char()
            if self.cur_char == '"' or self.cur_char is None:
                break
        return self.source[position:self.position]


    def next_token(self):
        token: Token = None
        
        self.__read_whitespace()

        match self.cur_char:
            case '+':
                token = self.__new_token(TokenType.PLUS, self.cur_char)
            case '-':
                if self.__next_char(1) == '>':
                    ch = self.cur_char
                    self.__read_char()
                    token = self.__new_token(TokenType.ARROW, ch + self.cur_char)
                else: 
                    token = self.__new_token(TokenType.MINUS, self.cur_char)
                
            case '*':
                token = self.__new_token(TokenType.MULTIPLY, self.cur_char)
            case '/':
                token = self.__new_token(TokenType.DIVIDE, self.cur_char)
            case '^':
                token = self.__new_token(TokenType.POW, self.cur_char)
            case '%':
                token = self.__new_token(TokenType.PERCENT, self.cur_char)
            case '(':
                token = self.__new_token(TokenType.LPAREN, self.cur_char)
            case ')':
                token = self.__new_token(TokenType.RPAREN, self.cur_char)
            case ',':
                token = self.__new_token(TokenType.COMMA, self.cur_char)
            case '{':
                token = self.__new_token(TokenType.LBRACE, self.cur_char)
            case '}':
                token = self.__new_token(TokenType.RBRACE, self.cur_char)
            case '<':
                if self.__next_char(1) == '=':
                    ch = self.cur_char
                    self.__read_char()
                    token = self.__new_token(TokenType.LESS_EQ, ch + self.cur_char)
                else:
                    token = self.__new_token(TokenType.LESS, self.cur_char)
            case '>':
                if self.__next_char(1) == '=':
                    ch = self.cur_char
                    self.__read_char()
                    token = self.__new_token(TokenType.GREATER_EQ, ch + self.cur_char)
                else:
                    token = self.__new_token(TokenType.GREATER, self.cur_char)
            case '=':
                if self.__next_char(1) == '=':
                    ch = self.cur_char
                    self.__read_char()
                    token = self.__new_token(TokenType.DOUBLE_EQ, ch + self.cur_char)
                else:
                    token = self.__new_token(TokenType.EQ, self.cur_char)
            case '!':
                if self.__next_char(1) == '=':
                    ch = self.cur_char
                    self.__read_char()
                    token = self.__new_token(TokenType.NOT_EQ, ch + self.cur_char)
                else:
                    #TODO
                    token = self.__new_token(TokenType.UNKNOWN, self.cur_char)
            case ';':
                token = self.__new_token(TokenType.SEPARATOR, self.cur_char) 
            case ':':
                token = self.__new_token(TokenType.COLON, self.cur_char) 
            case '"':
                token = self.__new_token(TokenType.STRING, self.__read_str())
            case '🤙':
                token = self.__new_token(TokenType.COLON, self.cur_char) 
            case None:
                token = self.__new_token(TokenType.EOF, "")
            case _:
                if self.__is_letter(self.cur_char):
                    literal: str = self.__read_indentifier()
                    type_ = lookup_ident(literal)
                    token = self.__new_token(type_,literal)
                    return token
                elif self.__is_digit(self.cur_char):
                    token = self.__read_number()
                    return token
                else:
                    token = self.__new_token(TokenType.UNKNOWN, self.cur_char)

        self.__read_char()
        return token
                    


