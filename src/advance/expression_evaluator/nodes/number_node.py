'''Python Class Number_Node

Number_Node used to represent a number
Only stores the token and value
'''
# Import Token and AST
from ..tokens import Token
from .ast import AST

class Number_Node(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = self.token.value
