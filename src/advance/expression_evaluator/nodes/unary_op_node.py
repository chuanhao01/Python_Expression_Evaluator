'''Python Class Unary_Node

Unary_Node used to represent unary operations like negative
Has a child, which represents the node to do the operation on
'''
# Import Token and AST
from ..tokens import Token
from .ast import AST

class UnaryOp_Node(AST):
    def __init__(self, token: Token, child: AST):
        self.token = token
        self.child = child