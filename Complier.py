from llvmlite import ir

from AST import Node, NodeType, Statement, Expression, Program
from AST import ExpressionStatement, VarStatement, ReturnStatement, BlockStatement, DefStatement, AssignmentStatement, IfStatement, WhileStatement, ForStatement, BreakStatement, ContinueStatement, ImportStatement
from AST import InfixExpression, CallExpression, PrefixExpression
from AST import IntLiteral, FloatLiteral, IdentifierLiteral, BoolLiteral
from AST import DefParam

from Enviroment import Enviroment
import os

from lexer import Lexer
from parser import Parser

class Compiler():
    def __init__(self):
        self.type_map: dict[str, ir.Type] = {
            "int": ir.IntType(32),
            "float": ir.FloatType(),
            "int52": ir.IntType(32), # TODO make int 64
            "float69": ir.FloatType(),
            "bool": ir.IntType(1),
            "void": ir.VoidType(),
            "str": ir.PointerType(ir.IntType(8))
        }

        self.module: ir.Module = ir.Module("main")
        self.builder: ir.IRBuilder = ir.IRBuilder()
        self.env: Enviroment = Enviroment()
        self.errors: list[str] = []
        self.counter = 0
        self.__initialize_builtins()

        self.breaks: list[ir.Block] = []
        self.continues: list[ir.Block] = []
        self.global_imports: dict[str, Program] = {}

    def __increment_counter(self):
        self.counter += 1
        return self.counter
    
    def __initialize_builtins(self):
        def __initialize_print():
            def_type = ir.FunctionType(self.type_map["int"], [ir.IntType(8).as_pointer()], var_arg=True)
            return ir.Function(self.module, def_type, 'printf')

        def __initialize_bools():
            bool_type: ir.Type = self.type_map["bool"]

            true_var = ir.GlobalVariable(self.module, bool_type, "true")
            true_var.initializer = ir.Constant(bool_type, 1)
            true_var.global_constant = True

            false_var = ir.GlobalVariable(self.module, bool_type, "false")
            false_var.initializer = ir.Constant(bool_type, 0)
            false_var.global_constant = True

            return true_var, false_var
        
        self.env.define("print", __initialize_print(), ir.IntType(32))
        
        true_var, false_var = __initialize_bools()
        self.env.define("true", true_var, true_var.type)
        self.env.define("false", false_var, false_var.type)

    def __convert_str(self, string:str):
        string = string.replace("\\n", "\n\0")
        f_string = f"{string}\0"
        c_string = ir.Constant(ir.ArrayType(ir.IntType(8), len(f_string)), bytearray(f_string.encode("utf8")))

        global_str = ir.GlobalVariable(self.module, c_string.type, name=f"__str_{self.__increment_counter()}")
        global_str.global_constant = True
        global_str.initializer = c_string
        global_str.linkage = "internal"
        return global_str, global_str.type

    def __builtin_print(self, params: list[ir.Instruction], ret_type: ir.Type):
        def_,_ = self.env.lookup("print")
        c_string = self.builder.alloca(ret_type)
        self.builder.store(params[0], c_string)
        rest_params = params[1:]
        if isinstance(params[0], ir.LoadInstr):
            c_fmt: ir.LoadInstr = params[0]
            ptr = c_fmt.operands[0]
            str_val = self.builder.load(ptr)
            fmt_arg = self.builder.bitcast(str_val, ir.IntType(8).as_pointer())
            return self.builder.call(def_, [fmt_arg, *rest_params])
        else:
            fmt_arg = self.builder.bitcast(self.module.get_global(f"__str_{self.counter}"), ir.IntType(8).as_pointer())
            return self.builder.call(def_,[fmt_arg, *rest_params])


    def compile(self, node: Node):
        match node.type_():
            case NodeType.PROGRAM:
                self.__visit_program(node)
            # statements
            case NodeType.EXPRESSION_STATEMENT:
                self.__visit_expression_statement(node)
            case NodeType.VAR_STATEMENT:
                self.__visit_var_statement(node)
            case NodeType.DEF_STATEMENT:
                self.__visit_def_statement(node)
            case NodeType.BLOCK_STATEMENT:
                self.__visit_block_statement(node)
            case NodeType.RETURN_STATEMENT:
                self.__visit_return_statement(node)
            case NodeType.ASSIGNMENT_STATEMENT:
                self.__visit_ass_statement(node)
            case NodeType.IF_STATEMENT:
                self.__visit_if_statement(node)
            case NodeType.WHILE_STATEMENT:
                self.__visit_while_statement(node)
            case NodeType.FOR_STATEMENT:
                self.__visit_for_statement(node)
            case NodeType.BREAK_STATEMENT:
                self.__visit_break_statement(node)
            case NodeType.CONTINUE_STATEMENT:
                self.__visit_continue_statement(node)
            case NodeType.IMPORT_STATEMENT:
                self.__visit_import_statement(node)

            #expressions
            case NodeType.INFIX_EXPRESSION:
                self.__visit_infix_expression(node)
            case NodeType.CALL_EXPRESSION:
                self.__visit_call_expression(node)

    # region helper funcs
    def __resolve_value(self, node: Expression, value_type: str = None) -> tuple[ir.Value, ir.Type]:
        match node.type_():
            case NodeType.INT_LITERAL:
                value, type_ = node.int, self.type_map["int" if value_type is None else value_type]
                return ir.Constant(type_, value), type_
            case NodeType.FLOAT_LITERAL:
                value, type_ = node.float, self.type_map["float" if value_type is None else value_type]
                return ir.Constant(type_, value), type_
            case NodeType.INDENTIFIER_LITERAL:
                ptr, type_ = self.env.lookup(node.value)
                return self.builder.load(ptr), type_
            case NodeType.BOOL_LITERAL:
                return ir.Constant(ir.IntType(1), 1 if node.value else 0), ir.IntType(1)
            case NodeType.STRING_LITERAL:
                string, type_ = self.__convert_str(node.value)
                return string, type_
            
            # expressions
            case NodeType.INFIX_EXPRESSION:
                return self.__visit_infix_expression(node)
            case NodeType.CALL_EXPRESSION:
                return self.__visit_call_expression(node)
            case NodeType.PREFIX_EXPRESSION:
                return self.__visit_prefix_epxression(node)



    # endregion

    # visit funcs
    def __visit_program(self, node: Program):
        # func_name = "main"
        # func_params: list[ir.Type] = []
        # func_return: ir.Type = self.type_map["int"]

        # fn_type = ir.FunctionType(func_return, func_params)
        # func = ir.Function(self.module, fn_type, func_name)

        # block = func.append_basic_block(f"{func_name}_entry")

        # self.builder = ir.IRBuilder(block)

        for stm in node.statements:
            self.compile(stm)

        # return_value: ir.Constant = ir.Constant(self.type_map["int"], 52)
        # self.builder.ret(return_value)

    def __visit_expression_statement(self, node: ExpressionStatement):
        self.compile(node.expr)

    def __visit_infix_expression(self, node: InfixExpression):
        op: str = node.op
        left_value, left_type = self.__resolve_value(node.l_node)
        right_value, right_type = self.__resolve_value(node.r_node)

        value = None
        type_ = None
        if isinstance(left_type, ir.IntType) and isinstance(right_type, ir.IntType):
            type_ =  self.type_map["int"]
            match op:
                case "+":
                    value = self.builder.add(left_value, right_value)
                case "-":
                    value = self.builder.sub(left_value, right_value)
                case "*":
                    value = self.builder.mul(left_value, right_value)
                case "/":
                    value = self.builder.sdiv(left_value, right_value)
                case "%":
                    value = self.builder.srem(left_value, right_value)
                case "^":
                    # TODO
                    pass
                case "<":
                    value = self.builder.icmp_signed("<", left_value, right_value)
                    type_ = ir.IntType(1)
                case ">":
                    value = self.builder.icmp_signed(">", left_value, right_value)
                    type_ = ir.IntType(1)
                case "<=":
                    value = self.builder.icmp_signed("<=", left_value, right_value)
                    type_ = ir.IntType(1)
                case ">=":
                    value = self.builder.icmp_signed(">=", left_value, right_value)
                    type_ = ir.IntType(1)
                case "==":
                    value = self.builder.icmp_signed("==", left_value, right_value)
                    type_ = ir.IntType(1)
                
        elif isinstance(left_type, ir.FloatType) and isinstance(right_type, ir.FloatType):
            type_ = self.type_map["float"]
            match op:
                case "+":
                    value = self.builder.fadd(left_value, right_value)
                case "-":
                    value = self.builder.fsub(left_value, right_value)
                case "*":
                    value = self.builder.fmul(left_value, right_value)
                case "/":
                    value = self.builder.fdiv(left_value, right_value)
                case "%":
                    value = self.builder.frem(left_value, right_value)
                case "^":
                    # TODO
                    pass
                case "<":
                    value = self.builder.fcmp_ordered("<", left_value, right_value)
                    type_ = ir.IntType(1)
                case ">":
                    value = self.builder.fcmp_ordered(">", left_value, right_value)
                    type_ = ir.IntType(1)
                case "<=":
                    value = self.builder.fcmp_ordered("<=", left_value, right_value)
                    type_ = ir.IntType(1)
                case ">=":
                    value = self.builder.fcmp_ordered(">=", left_value, right_value)
                    type_ = ir.IntType(1)
                case "==":
                    value = self.builder.fcmp_ordered("==", left_value, right_value)
                    type_ = ir.IntType(1)

        return value, type_
    
    def __visit_break_statement(self, node):
        self.builder.branch(self.breaks[-1])

    def __visit_continue_statement(self, node):
        self.builder.branch(self.continues[-1])

    def __visit_import_statement(self, node: ImportStatement):
        file_path:str = node.file_path
        if self.global_imports.get(file_path) is not None:
            print(f"file {file_path} is alredy fucking imported like bro actually can you just look at the code \n you ever tried thinking yk like actually this is insane \n you need to change like bro this is not okay")
            return
        with open(os.path.abspath(f"./{file_path}"), "r") as f:
            imp_code = f.read()
        l:Lexer = Lexer(source=imp_code)
        p:Parser = Parser(lexer=l)
        program:Program = p.parse_program()
        if len(p.errors) > 0:
            print(f"that fucking {file_path} is so ASS")
            for e in p.errors:
                print(e)
            exit()

        self.compile(node=program)
        self.global_imports[file_path] = program
    
    def __visit_for_statement(self, node:ForStatement):
        var_decl: VarStatement = node.var_decl
        condition: Expression = node.condition
        op: AssignmentStatement = node.op
        block: BlockStatement = node.block

        prev_env = self.env
        self.evn = Enviroment(parent=prev_env)
        self.compile(var_decl)

        for_entr = self.builder.append_basic_block(f"for_entr_{self.__increment_counter()}")
        for_other = self.builder.append_basic_block(f"for_other_{self.__increment_counter()}")
        self.breaks.append(for_other)
        self.continues.append(for_entr) # not working TODO

        self.builder.branch(for_entr)
        self.builder.position_at_start(for_entr)
        self.compile(block)
        self.compile(op)
        test,_ = self.__resolve_value(condition)
        self.builder.cbranch(test, for_entr, for_other)
        self.builder.position_at_start(for_other)
        self.breaks.pop()
        self.continues.pop()


    
    def __visit_while_statement(self, node):
        condition: Expression = node.condition
        block: BlockStatement = node.block
        test, _ = self.__resolve_value(condition)

        while_entr = self.builder.append_basic_block(f"while_entry_{self.__increment_counter()}")
        while_other = self.builder.append_basic_block(f"while_otherwise_{self.counter}")

        self.builder.cbranch(test, while_entr, while_other)
        self.builder.position_at_start(while_entr)
        self.compile(block)
        test,_ = self.__resolve_value(condition)
        self.builder.cbranch(test, while_entr, while_other)
        self.builder.position_at_start(while_other)
    
    def __visit_call_expression(self, node: CallExpression):
        name: str = node.def_.value
        params: list[Expression] = node.args
        args = []
        types = []

        if len(params) > 0:
            for p in params:
                p_val, p_type = self.__resolve_value(p)
                args.append(p_val)
                types.append(p_type)
        match name:
            case "print":
                out = self.__builtin_print(params=args, ret_type=types[0])
                ret_type = self.type_map["int"]
            case _:
                def_, ret_type = self.env.lookup(name)
                out = self.builder.call(def_, args)

        return out, ret_type
    
    def __visit_prefix_epxression(self, node: PrefixExpression):
        op: str = node.op
        r_node:Expression = node.r_node
        r_val, r_type = self.__resolve_value(r_node)

        Type = None
        Value = None
        if isinstance(r_type, ir.FloatType):
            Type = ir.FloatType()
            match op:
                case "-":
                    Value = self.builder.fmul(r_val, ir.Constant(ir.FloatType(), -1.0))
                case "!":
                    Value = ir.Constant(ir.IntType(1), 0)
        elif isinstance(r_type, ir.IntType):
            Type = ir.IntType(32)
            match op:
                case "-":
                    Value = self.builder.mul(r_val, ir.Constant(ir.IntType(32), -1))
                case "!":
                    Value = self.builder.not_(r_val)
        return Value, Type
    
    def __visit_var_statement(self, node:VarStatement):
        name: str = node.name.value
        value: Expression = node.value
        value_type: str = node.value_type # TODO

        value, type_ = self.__resolve_value(node=value, value_type=value_type)

        if self.env.lookup(name) is None:
            ptr = self.builder.alloca(type_)
            self.builder.store(value,ptr)
            self.env.define(name, ptr, type_)
        else:
            ptr, _ = self.env.lookup(name)
            self.builder.store(value, ptr)

    def __visit_block_statement(self, node: BlockStatement):
        for stm in node.statements:
            self.compile(stm)

    def __visit_return_statement(self, node:ReturnStatement):
        value: Expression = node.ret_value
        value, type_ = self.__resolve_value(value)

        self.builder.ret(value)
    
    def __visit_ass_statement(self, node: AssignmentStatement): # asssingment bro
        name:str = node.iden.value
        op:str = node.op
        new_value: Expression = node.new_value

        
        if self.env.lookup(name) is None:
            self.errors.append(f"bro you forgot to declare {name} before re-ASSinging it")
            return
        new_value, type_ = self.__resolve_value(new_value)
        val_ptr, _ = self.env.lookup(name)
        orig_val = self.builder.load(val_ptr)

        if isinstance(orig_val, ir.IntType) and isinstance(new_value, ir.FloatType):
            orig_val = self.builder.sitofp(orig_val, ir.FloatType)

        if isinstance(orig_val, ir.FloatType) and isinstance(new_value, ir.IntType):
            new_value = self.builder.sitofp(new_value, ir.FloatType)

        value = None
        Type = None
        match op:
            case "=":
                value = new_value
            case "+=":
                if isinstance(orig_val.type, ir.IntType) and isinstance(new_value.type, ir.IntType):
                    value = self.builder.add(orig_val, new_value)
                else:
                    value = self.builder.fadd(orig_val, new_value)
            case "-=":
                if isinstance(orig_val.type, ir.IntType) and isinstance(new_value.type, ir.IntType):
                    value = self.builder.sub(orig_val, new_value)
                else:
                    value = self.builder.fsub(orig_val, new_value)
            case "*=":
                if isinstance(orig_val.type, ir.IntType) and isinstance(new_value.type, ir.IntType):
                    value = self.builder.mul(orig_val, new_value)
                else:
                    value = self.builder.fmul(orig_val, new_value)
            case "/=":
                if isinstance(orig_val.type, ir.IntType) and isinstance(new_value.type, ir.IntType):
                    value = self.builder.sdiv(orig_val, new_value)
                else:
                    value = self.builder.fdiv(orig_val, new_value)
            case _:
                print("this ass operator is NOT supported")

        ptr,_ = self.env.lookup(name)
        self.builder.store(value, ptr)

    def __visit_if_statement(self, node: IfStatement):
        condition = node.condition
        true_block = node.true_block
        else_block = node.else_block

        test,_ = self.__resolve_value(condition)

        if else_block is None:
            with self.builder.if_then(test):
                self.compile(true_block)
        else:
            with self.builder.if_else(test) as (if_then, if_else):
                with if_then:
                    self.compile(true_block)
                with if_else:
                    self.compile(else_block)
                




    def __visit_def_statement(self, node:DefStatement):
        name:str = node.name.value
        block: BlockStatement = node.block
        params: list[DefParam] = node.params
        param_names: list[str] = [p.name for p in params]
        param_types: list[ir.Type] = [self.type_map[p.val_type] for p in params] 
        ret_type: ir.Type = self.type_map[node.ret_type]
        
        def_type: ir.FunctionType = ir.FunctionType(ret_type, param_types)
        def_: ir.Function = ir.Function(self.module, def_type, name)

        ir_block: ir.Block = def_.append_basic_block(f"{name}_entry")
        prev_builder = self.builder
        prev_env = self.env

        self.builder = ir.IRBuilder(ir_block)
        param_ptr = []
        for i,t in enumerate(param_types):
            ptr = self.builder.alloca(t)
            self.builder.store(def_.args[i], ptr)
            param_ptr.append(ptr)

        self.env = Enviroment(parent=prev_env)   

        for i,arg in enumerate(zip(param_types, param_names)):
            t = param_types[i]
            ptr = param_ptr[i]
            self.env.define(arg[1], ptr, t)
        self.env.define(name, def_, ret_type)
        self.compile(block)

        self.env = prev_env
        self.env.define(name, def_, ret_type)
        self.builder = prev_builder
        


    