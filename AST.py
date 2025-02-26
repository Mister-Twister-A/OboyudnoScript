from enum import Enum
from abc import ABC, abstractmethod

class NodeType(Enum):
    PROGRAM = "PROGRAM"

    # statements
    EXPRESSION_STATEMENT = "EXPRESSIONSTATEMENT"

    # expressions
    INFIX_EXPRESSION = "INFIXEXPRESSION"

    #literal
    INT_LITERAL = "INTLITERAL"
    FLOAT_LITERAL = "FLOATLITERAL"

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
        