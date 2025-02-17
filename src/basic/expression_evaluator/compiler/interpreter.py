
from ..tokens import PLUS, MINUS, MUL, DIV, POWER
from ..nodes import NodeVisitor
from .lexer import Lexer
from .parser import Parser

class Interpreter(NodeVisitor):
    def __error(self):
        raise Exception("Error interpreting expression.. Please try again")

    def visit_Number_Node(self, node):
        return node.token_value

    def visit_BinaryOp_Node(self, node):
        token_type = node.operator.token_type

        if token_type == PLUS:
            left_term = self.visit(node.left_term)
            right_term = self.visit(node.right_term)

            return left_term + right_term

        if token_type == MINUS:
            left_term = self.visit(node.left_term)
            right_term = self.visit(node.right_term)

            return left_term - right_term

        if token_type == MUL:
            left_term = self.visit(node.left_term)
            right_term = self.visit(node.right_term)

            return left_term * right_term

        if token_type == DIV:
            left_term = self.visit(node.left_term)
            right_term = self.visit(node.right_term)

            return left_term / right_term

        if token_type == POWER:
            left_term = self.visit(node.left_term)
            right_term = self.visit(node.right_term)

            return left_term ** right_term

        self.__error()

    def interpret(self):
        ast = self.parser.parse()

        if ast == None:
            return (None, None)

        return (ast, self.visit(ast))