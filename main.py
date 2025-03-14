import sys
import os
from lexer import Lexer
from parser import Parser
from AST import Program
import json
import time
from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float
from Complier import Compiler

#🤙
#python main.py test.🤙
file_path = sys.argv[1]

LEXER_DEBUG = False
PARSER_DEBUG = True
COMPILER_DEBUG = True
RUN_CODE = True
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

        if RUN_CODE:
            print("----------------running code-------------")
            llvm.initialize()
            llvm.initialize_native_target()
            llvm.initialize_native_asmprinter()

            try:
                llvm_ir_parsed = llvm.parse_assembly(str(module))
                llvm_ir_parsed.verify()
            except Exception as e:
                print(e)
                exit()
            
            tgt_machine = llvm.Target.from_default_triple().create_target_machine()
            engine = llvm.create_mcjit_compiler(llvm_ir_parsed, tgt_machine)
            engine.finalize_object()

            entry = engine.get_function_address("main")
            cfunc = CFUNCTYPE(c_int)(entry)
            st = time.time()
            res = cfunc()
            ed = time.time()

            print(f"\n Program returned fucking {res} \n finished in {round((ed - st) * 1000,6)} ms, you NEED to optimize your code dumbass")




