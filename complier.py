import sys
import os
from lexer import Lexer
from parser import Parser
from AST import Program
import json

#🤙
file_path = sys.argv[1]

LEXER_DEBUG = False
PARSER_DEBUG = True
with open(file_path, "r") as f:
    code = f.read()

    if LEXER_DEBUG:
        lexer = Lexer(code)
        while lexer.cur_char is not None:
            print(lexer.next_token())
    
    l: Lexer = Lexer(source=code)
    p: Parser = Parser(lexer=l)
    if PARSER_DEBUG:
        print("----------------parser debug----------------")
        program: Program = p.parse_program()

        with open("./debug/ast.json", "w") as f:
            json.dump(program.json(), f, indent=4)

        print("parser debug end")


