from enum import Enum
from typing import Any
#lol yay
class TokenType(Enum):
    #you are my specia
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"

    # data types
    INT = "INT"
    FLOAT = "FLOAT"

    #arithmetic
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    POW = "POW"
    PERCENT = "PERCENT"

    #symbols
    SEPARATOR = ";"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"


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
