from Token import Token, TokenType
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

    def __read_whitespace(self):
        while self.cur_char in [' ', '\t', '\r', '\n']:
            if self.cur_char == '\n':
                self.line_no +=1
            self.__read_char()

    def __new_token(self, type_: TokenType, literal: Any):
        return Token(type_,literal,self.line_no, self.position)
    
    def __is_digit(self, ch: str):
        return '0' <= ch and ch <= '9'
    
    def __read_number(self):
        start_pos : int = self.position
        num_dots : int = 0

        number : str = ""
        while self.__is_digit(self.cur_char) or self.cur_char == '.':
            if self.cur_char == '.':
                num_dots+=1

            if num_dots > 1:
                print(f"BAD NUMBER AT LINE {self.line_no} PLACE {self.position}")
                return self.__new_token(TokenType.UNKNOWN, self.source[start_pos:self.position])
            
            number+=self.cur_char
            self.__read_char()

            if self.cur_char is None:
                break

        if num_dots == 0:
            return self.__new_token(TokenType.INT, int(number))
        else: 
            return self.__new_token(TokenType.FLOAT, float(number))


    def next_token(self):
        token: Token = None
        
        self.__read_whitespace()

        match self.cur_char:
            case '+':
                token = self.__new_token(TokenType.PLUS, self.cur_char)
            case '-':
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
            case ';':
                token = self.__new_token(TokenType.SEPARATOR, self.cur_char)
            case None:
                token = self.__new_token(TokenType.EOF, "")
            case _:
                if self.__is_digit(self.cur_char):
                    token = self.__read_number()
                    return token
                else:
                    token = self.__new_token(TokenType.UNKNOWN, self.cur_char)

        self.__read_char()
        return token
                    


