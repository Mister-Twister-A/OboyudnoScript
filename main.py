import sys
import os
from lexer import Lexer
from parser import Parser
from AST import Program
import json
from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float
from Complier import Compiler

#🤙
#python main.py test.🤙
file_path = sys.argv[1]

LEXER_DEBUG = False
PARSER_DEBUG = False
COMPILER_DEBUG = True
if __name__ == "__main__":
    with open(file_path, "r") as f:
        code = f.read()

        if LEXER_DEBUG:
            lexer = Lexer(code)
            while lexer.cur_char is not None:
                print(lexer.next_token())
        
        l: Lexer = Lexer(source=code)
        p: Parser = Parser(lexer=l)
        program: Program = p.parse_program()
        if len(p.errors) > 0:
            for e in p.errors:
                print(e)
            exit()
        
        if PARSER_DEBUG:
            print("----------------parser debug----------------")
            with open("./debug/ast.json", "w") as f:
                json.dump(program.json(), f, indent=4)

            print("----------------parser debug end------------")
        
        compiler: Compiler = Compiler()
        compiler.compile(node=program)

        module: ir.Module = compiler.module
        module.triple = llvm.get_default_triple()

        if COMPILER_DEBUG:
            print("----------------compiler debug-------------")
            with open("./debug/ir.ll", "w") as f:
                f.write(str(module))
            print("----------------compiler debug end---------")


