
from ..tokens import PLUS, MINUS, MUL, DIV, POWER
from ..nodes import NodeVisitor
from .lexer import Lexer
from .parser import Parser

class Interpreter(NodeVisitor):
    def error(self):
        raise Exception("Error intepreting expression")

    def visit_Number_Node(self, node):
        return node.token_value

    def visit_BinaryOp_Node(self, node):
        token_type = node.operator.token_type

        if token_type == PLUS:
            return self.visit(node.left_term) + self.visit(node.right_term)
        if token_type == MINUS:
            return self.visit(node.left_term) - self.visit(node.right_term)
        if token_type == MUL:
            return self.visit(node.left_term) * self.visit(node.right_term)
        if token_type == DIV:
            return self.visit(node.left_term) / self.visit(node.right_term)
        if token_type == POWER:
            return self.visit(node.left_term) ** self.visit(node.right_term)

    def interpret(self):
        ast = self.parser.parse()

        #! If there was an error_msg returned from the parser
        if isinstance(ast, str):
            error_msg = ast
            return (None, error_msg)

        elif ast == None:
            return (None, None)

        return (ast, self.visit(ast))