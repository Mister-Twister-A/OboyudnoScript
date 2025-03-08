from Token import Token, TokenType
from lexer import Lexer
from enum import Enum, auto
from typing import Callable

from AST import Statement, Expression,Program
from AST import ExpressionStatement, VarStatement, DefStatement, BlockStatement, ReturnStatement, AssignmentStatement, IfStatement, WhileStatement
from AST import InfixExpression, CallExpression
from AST import IntLiteral, FloatLiteral, IdentifierLiteral, BoolLiteral, StringLiteral
from AST import DefParam



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
    TokenType.POW: Precedence.P_EXPONENT,
    TokenType.DOUBLE_EQ: Precedence.P_EQUAL,
    TokenType.NOT_EQ: Precedence.P_EQUAL,
    TokenType.LESS: Precedence.P_LESSGREATER,
    TokenType.GREATER: Precedence.P_LESSGREATER,
    TokenType.LESS_EQ: Precedence.P_LESSGREATER,
    TokenType.GREATER_EQ: Precedence.P_LESSGREATER,
    TokenType.LPAREN: Precedence.P_CALL,

}

class Parser():
    def __init__(self, lexer):
        self.lexer: Lexer = lexer
        self.errors: list[str] = []

        self.cur_token: Token = None
        self.next_token: Token = None

        self.prefix_parse_fn: dict[TokenType, Callable] = {
            TokenType.IDENTIFIER: self.__parse_identifier,
            TokenType.INT: self.__parse_int_literal,
            TokenType.FLOAT: self.__parse_float_literal,
            TokenType.LPAREN: self.__parse_group_expression,
            TokenType.IF: self.__parse_if_statement,
            TokenType.TRUE: self.__parse_bool,
            TokenType.FALSE: self.__parse_bool,
            TokenType.STRING: self.__parse_string_literal,
        } 
        self.infix_parse_fn: dict[TokenType, Callable] = {
            TokenType.PLUS: self.__parse_infix_expression,
            TokenType.MINUS: self.__parse_infix_expression,
            TokenType.MULTIPLY: self.__parse_infix_expression,
            TokenType.DIVIDE: self.__parse_infix_expression,
            TokenType.POW: self.__parse_infix_expression,
            TokenType.PERCENT: self.__parse_infix_expression,
            TokenType.DOUBLE_EQ: self.__parse_infix_expression,
            TokenType.NOT_EQ: self.__parse_infix_expression,
            TokenType.LESS: self.__parse_infix_expression,
            TokenType.GREATER: self.__parse_infix_expression,
            TokenType.LESS_EQ: self.__parse_infix_expression,
            TokenType.GREATER_EQ: self.__parse_infix_expression,
            TokenType.LPAREN: self.__parse_call_expression,

        } 

        self.__next_token()
        self.__next_token()

    #region Helper funcs

    def __next_token(self):
        self.cur_token = self.next_token
        self.next_token = self.lexer.next_token()

    def __next_token_is(self, type_: TokenType):
        return self.next_token.type == type_
    
    def __cur_token_is(self, type_: TokenType):
        return self.cur_token.type == type_
    
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
        if self.__cur_token_is(TokenType.IDENTIFIER) and self.__next_token_is(TokenType.EQ):
            return self.__parse_assignment_statement()

        match self.cur_token.type:
            case TokenType.VAR:
                return self.__parse_var_statement()
            case TokenType.DEF:
                return self.__parse_def_statement()
            case TokenType.RETURN:
                return self.__parse_ret_statement()
            case TokenType.WHILE:
                return self.__parse_while_statement()
            case _:
                return self.__parse_statement_expression()
            
    def __parse_while_statement(self):
        condition: Expression = None
        block: BlockStatement = None
        self.__next_token()
        condition = self.__parse_expression(Precedence.P_LOWEST)

        if not self.__expect_next(TokenType.LBRACE):
            return None
        block = self.__parse_block_statement()
        while_stm = WhileStatement(condition=condition, block=block)
        return while_stm

    
    def __parse_statement_expression(self):
        expr = self.__parse_expression(Precedence.P_LOWEST)

        if self.__next_token_is(TokenType.SEPARATOR):
            self.__next_token()

        stm: ExpressionStatement = ExpressionStatement(expr=expr)
        return stm
    
    def __parse_var_statement(self):
        # var a: int = 10;
        stm: VarStatement = VarStatement()

        if not self.__expect_next(TokenType.IDENTIFIER):
            return None
        
        stm.name = IdentifierLiteral(self.cur_token.literal)
        

        if not self.__expect_next(TokenType.COLON):
            return None
        if not self.__expect_next(TokenType.TYPE):
            return None
        
        stm.value_type = self.cur_token.literal

        if not self.__expect_next(TokenType.EQ):
            return None
        self.__next_token()
        stm.value = self.__parse_expression(Precedence.P_LOWEST)
        
        while not self.__cur_token_is(TokenType.SEPARATOR) and not self.__cur_token_is(TokenType.EOF):
            self.__next_token()
        return stm
    
    def __parse_assignment_statement(self):
        stm: AssignmentStatement = AssignmentStatement()
        # x = 5 + 5
        stm.iden = IdentifierLiteral(self.cur_token.literal)
        self.__next_token()
        self.__next_token()
        stm.new_value = self.__parse_expression(Precedence.P_LOWEST)

        self.__next_token()

        return stm


    
    def __parse_def_statement(self):
        def_stm: DefStatement = DefStatement()
        # def name() -> int { return x; }

        if not self.__expect_next(TokenType.IDENTIFIER):
            return None
        
        def_stm.name = IdentifierLiteral(self.cur_token.literal)

        if not self.__expect_next(TokenType.LPAREN):
            return None
        
        def_stm.params = self.__parse_def_params() 
        
        if not self.__expect_next(TokenType.ARROW):
            return None
        
        if not self.__expect_next(TokenType.TYPE):
            return None
        
        def_stm.ret_type = self.cur_token.literal

        if not self.__expect_next(TokenType.LBRACE):
            return None
        
        def_stm.block = self.__parse_block_statement()

        return def_stm
    
    def __parse_def_params(self):
        params: list[DefParam] = []
        if self.__next_token_is(TokenType.RPAREN):
            self.__next_token()
            return params
        
        self.__next_token()
        first_param = DefParam(name=self.cur_token.literal)
        if not self.__expect_next(TokenType.COLON):
            return None
        self.__next_token()
        first_param.val_type = self.cur_token.literal
        params.append(first_param)

        while self.__next_token_is(TokenType.COMMA):
            self.__next_token()
            self.__next_token()
            param: DefParam = DefParam(name=self.cur_token.literal)
            if not self.__expect_next(TokenType.COLON):
                return None
            self.__next_token()
            
            param.val_type = self.cur_token.literal

            params.append(param)
        if not self.__expect_next(TokenType.RPAREN):
            return None
        return params


    def __parse_ret_statement(self):
        stm: ReturnStatement = ReturnStatement()

        self.__next_token()
        stm.ret_value = self.__parse_expression(Precedence.P_LOWEST)

        if not self.__expect_next(TokenType.SEPARATOR):
            return None
        
        return stm
        
    def __parse_block_statement(self):
        block: BlockStatement = BlockStatement()
        self.__next_token()
        while not self.__cur_token_is(TokenType.RBRACE) and not self.__cur_token_is(TokenType.EOF):
            stm = self.__parse_statement()
            if stm is not None:
                block.statements.append(stm)

            self.__next_token()

        return block
    
    def __parse_if_statement(self):
        condition: Expression = None
        true_block: BlockStatement = None
        else_block: BlockStatement = None

        self.__next_token()
        condition = self.__parse_expression(Precedence.P_LOWEST)
        if not self.__expect_next(TokenType.LBRACE):
            return None
        true_block = self.__parse_block_statement()
        if self.__next_token_is(TokenType.ELSE):
            self.__next_token()
            if not self.__expect_next(TokenType.LBRACE):
                return None
            else_block = self.__parse_block_statement()

        if_stm = IfStatement(condition=condition, true_block=true_block, else_block=else_block)
        return if_stm

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
    
    def __parse_call_expression(self, def_: Expression):
        call_: CallExpression = CallExpression(def_=def_)
        call_.args = self.__parse_expr_list(TokenType.RPAREN)
        return call_
    
    def __parse_expr_list(self, end: TokenType):
        args: list[Expression] = []
        if self.__next_token_is(end):
            self.__next_token()
            return args
        
        self.__next_token()

        args.append(self.__parse_expression(Precedence.P_LOWEST))
        while self.__next_token_is(TokenType.COMMA):
            self.__next_token()
            self.__next_token()
            args.append(self.__parse_expression(Precedence.P_LOWEST))

        if not self.__expect_next(end):
            return None
        return args
        
    
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
    
    def __parse_string_literal(self):
        return StringLiteral(value=self.cur_token.literal)
    
    def __parse_identifier(self):
        return IdentifierLiteral(self.cur_token.literal)
    
    def __parse_bool(self):
        return BoolLiteral(value=self.__cur_token_is(TokenType.TRUE))


