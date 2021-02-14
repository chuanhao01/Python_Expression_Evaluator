'''Python Class BinaryOp_Node

BinaryOp Node represents a binary operation with a left and right expression
'''
# Import Token and AST
from ..tokens import Token
from .ast import AST

class BinaryOp_Node(AST):
    def __init__(self, token: Token, left: AST, right: AST):
        self.token = token
        self.left = left
        self.right = right