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
    def json_(self):
        pass


class Statement(Node):
    pass

class Expression(Node):
    pass

class Program(Node):
    def __init__(self):
        self.statements = []

    def type_(self):
        return NodeType.PROGRAM
    
    def json_(self):
        return {
            "type": self.type_().value,
            "statements": [{stm.type_().value: stm.json_()} for stm in self.statements]
        }

class ExpressionStatement(Statement):
    def __init__(self, expr: Expression = None):
        self.expr = expr

    def type_(self):
        return NodeType.EXPRESSION_STATEMENT
    
    def json_(self):
        return {
            "type" : self.type_().value,
            "json" : self.expr.json_()
        }

