from llvmlite import ir

from AST import Node, NodeType, Statement, Expression, Program
from AST import ExpressionStatement, InfixExpression
from AST import IntLiteral, FloatLiteral

class Compiler():
    def __init__(self):
        self.type_map: dict[str, ir.Type] = {
            "int": ir.IntType(32),
            "float": ir.FloatType()
        }

        self.module: ir.Module = ir.Module("main")
        self.builder: ir.IRBuilder = ir.IRBuilder()

    def compile(self, node: Node):
        match node.type_():
            case NodeType.PROGRAM:
                self.__visit_program(node)
            # statements
            case NodeType.EXPRESSION_STATEMENT:
                self.__visit_expression_statement(node)
            
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
            
            # expressions
            case NodeType.INFIX_EXPRESSION:
                return self.__visit_infix_expression(node)



    # endregion

    # visit funcs
    def __visit_program(self, node: Program):
        func_name = "main"
        func_params: list[ir.Type] = []
        func_return: ir.Type = self.type_map["int"]

        fn_type = ir.FunctionType(func_return, func_params)
        func = ir.Function(self.module, fn_type, func_name)

        block = func.append_basic_block(f"{func_name}_entry")

        self.builder = ir.IRBuilder(block)

        for stm in node.statements:
            self.compile(stm)

        return_value: ir.Constant = ir.Constant(self.type_map["int"], 52)
        self.builder.ret(return_value)

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

    