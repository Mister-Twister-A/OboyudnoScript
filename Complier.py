from llvmlite import ir

from AST import Node, NodeType, Statement, Expression, Program
from AST import ExpressionStatement, VarStatement, ReturnStatement, BlockStatement, DefStatement
from AST import InfixExpression
from AST import IntLiteral, FloatLiteral, IdentifierLiteral

from Enviroment import Enviroment

class Compiler():
    def __init__(self):
        self.type_map: dict[str, ir.Type] = {
            "int": ir.IntType(32),
            "float": ir.FloatType(),
            "int52": ir.IntType(64),
            "float69": ir.FloatType()
        }

        self.module: ir.Module = ir.Module("main")
        self.builder: ir.IRBuilder = ir.IRBuilder()
        self.env: Enviroment = Enviroment()

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

            
            #expressions
            case NodeType.INFIX_EXPRESSION:
                self.__visit_infix_expression(node)

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
            
            # expressions
            case NodeType.INFIX_EXPRESSION:
                return self.__visit_infix_expression(node)



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

        return value, type_
    
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

    def __visit_def_statement(self, node:DefStatement):
        name:str = node.name.value
        block: BlockStatement = node.block
        params: list[IdentifierLiteral] = node.params
        param_names: list[str] = [p.value for p in params]
        param_types: list[ir.Type] = [] # TODO
        ret_type: ir.Type = self.type_map[node.ret_type]
        
        def_type: ir.FunctionType = ir.FunctionType(ret_type, param_types)
        def_: ir.Function = ir.Function(self.module, def_type, name)

        ir_block: ir.Block = def_.append_basic_block(f"{name}_entry")
        prev_builder = self.builder
        prev_env = self.env

        self.builder = ir.IRBuilder(ir_block)

        self.env = Enviroment(parent=self.env)
        self.env.define(name, def_, ret_type)
        self.compile(block)

        self.env = prev_env
        self.env.define(name, def_, ret_type)
        self.builder = prev_builder
        


    