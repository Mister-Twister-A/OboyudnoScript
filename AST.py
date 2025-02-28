from enum import Enum
from abc import ABC, abstractmethod

class NodeType(Enum):
    PROGRAM = "PROGRAM"

    # statements
    EXPRESSION_STATEMENT = "EXPRESSIONSTATEMENT"
    VAR_STATEMENT = "VARSTATEMENT"
    BLOCK_STATEMENT = "BLOCK_STATEMENT"
    RETURN_STATEMENT = "RETURN_STATEMENT"
    DEF_STATEMENT = "DEF_STATEMENT"

    # expressions
    INFIX_EXPRESSION = "INFIXEXPRESSION"

    #literal
    INT_LITERAL = "INTLITERAL"
    FLOAT_LITERAL = "FLOATLITERAL"
    INDENTIFIER_LITERAL = "INDENTIFIERLITERAL"

class Node(ABC):
    @abstractmethod
    def type_(self) -> NodeType:
        pass

    @abstractmethod
    def json(self):
        pass


class Statement(Node):
    pass

class Expression(Node):
    pass

class Program(Node):
    def __init__(self):
        self.statements: list[Statement] = []

    def type_(self):
        return NodeType.PROGRAM
    
    def json(self):
        return {
            "type": self.type_().value,
            "statements": [{stm.type_().value: stm.json()} for stm in self.statements]
        }


# statements

class ExpressionStatement(Statement):
    def __init__(self, expr: Expression = None):
        self.expr = expr

    def type_(self):
        return NodeType.EXPRESSION_STATEMENT
    
    def json(self):
        return {
            "type" : self.type_().value,
            "json" : self.expr.json()
        }

    
class VarStatement(Statement):
    def __init__(self, name: Expression = None, value: Expression = None, value_type:str = None):
        self.name = name
        self.value = value
        self.value_type = value_type

    def type_(self):
        return NodeType.VAR_STATEMENT
    
    def json(self):
        return {
            "type": self.type_().value,
            "name": self.name.json(),
            "value": self.value.json(),
            "value_type": self.value_type
        }
    

class BlockStatement(Statement):
    def __init__(self, statements: list[Statement] = None):
        self.statements = statements if statements is not None else []

    def type_(self):
        return NodeType.BLOCK_STATEMENT
    
    def json(self):
        return {
            "type": self.type_().value,
            "statements": [stm.json() for stm in self.statements]
        }
    

class ReturnStatement(Statement):
    def __init__(self, ret_value: Expression = None):
        self.ret_value = ret_value

    def type_(self):
        return NodeType.RETURN_STATEMENT
    
    def json(self):
        return {
            "type": self.type_().value,
            "ret_value": self.ret_value.json()

        }


class DefStatement(Statement):
    def __init__(self, name = None, params:list = None, ret_type:str = None, block: BlockStatement = None):
        self.name = name
        self.params = params
        self.block = block
        self.ret_type = ret_type

    def type_(self):
        return NodeType.DEF_STATEMENT
    
    def json(self):
        return {
            "type": self.type_().value,
            "name": self.name.json(),
            "params": [p.json() for p in self.params],
            "ret_type": self.ret_type,
            "block": self.block.json()
        }
        

# expressions
class InfixExpression(Expression):
    def __init__(self, l_node: Expression, op: str, r_node: Expression = None):
        self.l_node: Expression = l_node
        self.op: str = op
        self.r_node: Expression = r_node

    def type_(self):
        return NodeType.INFIX_EXPRESSION
    
    def json(self):
        return {
            "type": self.type_().value,
            "left_node": self.l_node.json(),
            "operator": self.op,
            "r_node": self.r_node.json()

        }

        
# litarals
class IntLiteral(Expression):
    def __init__(self, value: int = None):
        self.int: int = value

    def type_(self):
        return NodeType.INT_LITERAL
    
    def json(self):
        return {
            "type": self.type_().value,
            "value": self.int
        }


class FloatLiteral(Expression):
    def __init__(self, value: float = None):
        self.float: float = value

    def type_(self):
        return NodeType.FLOAT_LITERAL
    
    def json(self):
        return {
            "type": self.type_().value,
            "value": self.float
        }
    

class IdentifierLiteral(Expression):
    def __init__(self, value: str = None):
        self.value: str = value

    def type_(self):
        return NodeType.INDENTIFIER_LITERAL
    
    def json(self):
        return {
            "type": self.type_().value,
            "value": self.value
        }
        