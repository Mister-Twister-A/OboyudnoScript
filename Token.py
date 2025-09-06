from enum import Enum
from typing import Any
#lol yay
class TokenType(Enum):
    #you are my specia
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"

    # data types
    IDENTIFIER = "IDENTIFIER"
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"

    #arithmetic
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    POW = "POW"
    PERCENT = "PERCENT"

    #assigmenty symbols
    EQ = "EQ"
    PLUS_EQ = "PLUS_EQ"
    MINUS_EQ = "MINUS_EQ"
    MUL_EQ = "MUL_EQ"
    DIV_EQ = "DIV_EQ"

    # bool symbols
    LESS = "<"
    GREATER = ">"
    DOUBLE_EQ = "=="
    GREATER_EQ = ">="
    LESS_EQ = "<="
    NOT_EQ = "!="

    #symbols
    ARROW = "ARROW"
    COLON = ":"
    COMMA = ","
    SEPARATOR = ";"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    NOT = "NOT"

    #key words
    VAR = "VAR"
    DEF = "DEF"
    RETURN = "RETURN"
    IF = "IF"
    ELSE = "ELSE"
    TRUE = "TRUE"
    FALSE = "FALSE"
    WHILE = "WHILE"
    FOR = "FOR"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    IMPORT = "IMPORT"

    # type
    TYPE = "TYPE"


class Token():
    def __init__(self, token_type: TokenType, literal: Any, n_row:int, place:int):
        self.type = token_type
        self.literal = literal # the value 
        self.row = n_row
        self.place = place
    
    def __str__(self):
        return f"Token {self.type} : {self.literal} ; Row {self.row}, Place {self.place}"
    
    def __repr__(self):
        return str(self)
    
KEYWORDS: dict[str, TokenType] = {
    "var": TokenType.VAR,
    "def": TokenType.DEF,
    "return": TokenType.RETURN,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "import": TokenType.IMPORT,

}

OBOYUDNO_KEYWORDS: dict[str, TokenType] = {
    "oboyudno": TokenType.VAR,
    "los_tungtungtungtungritas": TokenType.VAR,
    "🤙": TokenType.COLON,
    "real": TokenType.SEPARATOR,
    "basil_seed": TokenType.DEF,
    "fuck_you": TokenType.RETURN,
    "B--D": TokenType.ARROW,
    "ye": TokenType.IF,
    "elsagate": TokenType.ELSE,
    "poka": TokenType.WHILE,
    "dlya": TokenType.FOR,
    "fucking_die": TokenType.BREAK,
    "long_live_the_king": TokenType.CONTINUE,
    "get_over_here": TokenType.IMPORT,

}

TYPE_KEYWORDS: list[str] = ["int", "float", "int52", "float69", "str", "void"]

def lookup_ident(ident: str):
    type_: TokenType | None = KEYWORDS.get(ident)
    if type_ is not None:
        return type_
    type_: TokenType | None = OBOYUDNO_KEYWORDS.get(ident)
    if type_ is not None:
        return type_
    if ident in TYPE_KEYWORDS:
        return TokenType.TYPE
    
    return TokenType.IDENTIFIER
