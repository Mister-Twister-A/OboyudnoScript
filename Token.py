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

    #arithmetic
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    POW = "POW"
    PERCENT = "PERCENT"

    #assigmenty symbols
    EQ = "EQ"
    

    #symbols
    ARROW = "ARROW"
    COLON = ":"
    SEPARATOR = ";"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"

    #key words
    VAR = "VAR"
    DEF = "DEF"
    RETURN = "RETURN"

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
    "return": TokenType.RETURN
}

OBOYUDNO_KEYWORDS: dict[str, TokenType] = {
    "oboyudno": TokenType.VAR,
    "🤙": TokenType.COLON,
    "real": TokenType.SEPARATOR,
    "basil": TokenType.DEF,
    "fuck_you": TokenType.RETURN,
    "B--D": TokenType.ARROW,
}

TYPE_KEYWORDS: list[str] = ["int", "float", "int52", "float69"]

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
