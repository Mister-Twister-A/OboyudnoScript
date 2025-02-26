from Token import Token, TokenType
from lexer import Lexer
from enum import Enum, auto
from typing import Callable

from AST import Statement, Expression,Program
from AST import ExpressionStatement
from AST import InfixExpression
from AST import IntLiteral, FloatLiteral



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

        self.prefix_parse_fn: dict[TokenType, Callable] = {
            TokenType.INT: self.__parse_int_literal,
            TokenType.FLOAT: self.__parse_float_literal,
            TokenType.LPAREN: self.__parse_group_expression
        } 
        self.infix_parse_fn: dict[TokenType, Callable] = {
            TokenType.PLUS: self.__parse_infix_expression,
            TokenType.MINUS: self.__parse_infix_expression,
            TokenType.MULTIPLY: self.__parse_infix_expression,
            TokenType.DIVIDE: self.__parse_infix_expression,
            TokenType.POW: self.__parse_infix_expression,
            TokenType.PERCENT: self.__parse_infix_expression,

        } 

        self.__next_token()
        self.__next_token()

    #region Helper funcs

    def __next_token(self):
        self.cur_token = self.next_token
        self.next_token = self.lexer.next_token()

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

    def __expect_next(self, type_: TokenType):
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
        program: Program = Program()
        while self.cur_token.type != TokenType.EOF:
            stm: Statement = self.__parse_statement()
            if stm is not None:
                program.statements.append(stm)

            self.__next_token()

        return program
    
    def __parse_statement(self):
        return self.__parse_statement_expression()
    
    def __parse_statement_expression(self):
        expr = self.__parse_expression(Precedence.P_LOWEST)

        if self.__next_token_is(TokenType.SEPARATOR):
            self.__next_token()

        stm: ExpressionStatement = ExpressionStatement(expr=expr)
        return stm
    
    def __parse_expression(self, precedence: Precedence):
        prefix_fn: Callable | None = self.prefix_parse_fn.get(self.cur_token.type) 

        if prefix_fn is None:
            self.__no_prefix_prase_fn_error(self.cur_token.type)
            return None
        
        left_expr: Expression = prefix_fn()
        while not self.__next_token_is(TokenType.SEPARATOR) and precedence.value < self.__next_precedence().value:
            infix_fn: Callable | None = self.infix_parse_fn.get(self.next_token.type)
            if infix_fn is None:
                return left_expr
            
            self.__next_token()

            left_expr = infix_fn(left_expr)

        return left_expr

    def __parse_infix_expression(self, l_node: Expression):
        infix: InfixExpression = InfixExpression(l_node=l_node, op=self.cur_token.literal)

        precedence = self.__cur_precedence()

        self.__next_token()

        infix.r_node = self.__parse_expression(precedence)

        return infix
    
    def __parse_group_expression(self):
        self.__next_token()

        expr: Expression = self.__parse_expression(Precedence.P_LOWEST)
        if not self.__expect_next(TokenType.RPAREN):
            return None
        
        return expr
    
    def __parse_int_literal(self):
        int_node: IntLiteral = IntLiteral()

        try:
            int_node.int = int(self.cur_token.literal)
        except:
            self.errors.append(f"That shit is NOT an int, just look at it {self.cur_token.literal}")
            return None
        
        return int_node
    
    def __parse_float_literal(self):
        float_node: FloatLiteral = FloatLiteral()

        try:
            float_node.float = float(self.cur_token.literal)
        except:
            self.errors.append(f"Never in ANY fucking circumstaces thats a float, look at if {self.cur_token.literal}")
            return None
        
        return float_node


