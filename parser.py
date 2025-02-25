from Token import Token, TokenType
from lexer import Lexer
from enum import Enum, auto
from typing import Callable

class Precedence(Enum):

    P_LOWEST = 0
    P_EQUAL = auto()
    P_LESSGREATER = auto()
    P_SUM = auto()
    P_PRODUCT = auto()
    P_EXPONENT = auto()
    P_PREFIX = auto()
    P_CALL = auto()
    P_INDEX = auto()

PRECEDENCES : dict[TokenType, Precedence] = {
    TokenType.PLUS: Precedence.P_SUM,
    TokenType.MINUS: Precedence.P_SUM,
    TokenType.MULTIPLY: Precedence.P_PRODUCT,
    TokenType.DIVIDE: Precedence.P_PRODUCT,
    TokenType.PERCENT: Precedence.P_PRODUCT,
    TokenType.POW: Precedence.P_EXPONENT
}

class Parser():
    def __init__(self, lexer):
        self.lexer: Lexer = lexer
        self.errors: list[str] = []

        self.cur_token: Token = None
        self.next_token: Token = None

        self.prefix_parse_fn: dict[TokenType, Callable] = {} # -5
        self.infix_parse_fn: dict[TokenType, Callable] = {} # 5 + 5

        self.__next_token()
        self.__next_token()

    #region Helper funcs

    def __next_token(self):
        self.cur_token = self.next_token
        self.next_token = self.lexer.next_token

    def __next_token_is(self, type_: TokenType):
        return self.next_token.type == type_
    
    def __cur_precedence(self):
        prec: Precedence | None =  PRECEDENCES.get(self.cur_token.type)
        if prec == None:
            prec = Precedence.P_LOWEST
        return prec
    
    def __next_precedence(self):
        prec: Precedence | None =  PRECEDENCES.get(self.next_token.type)
        if prec == None:
            prec = Precedence.P_LOWEST
        return prec

    def __expect_peek(self, type_: TokenType):
        if self.__next_token_is(type_):
            self.__next_token()
            return True
        else:
            self.__expect_error(type_)
            return False
    
    def __expect_error(self, type_: TokenType):
        self.errors.append(f"expected the next fucking token to be fucking {type_} but got fucking {self.next_token.type} instead")

    def __no_prefix_prase_fn_error(self, type_: TokenType):
        self.errors.append(f"no stupid prefix parse function found for {type_}, you are EXTREAMLY stupid")

    #endregion

    def parse_program(self):
        pass