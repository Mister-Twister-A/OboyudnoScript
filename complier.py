import sys
import os
from lexer import Lexer

#🤙
file_path = sys.argv[1]
with open(file_path, "r") as f:
    code = f.read()

    lexer = Lexer(code)
    while lexer.cur_char is not None:
        print(lexer.next_token())


