'''Python Class String_Node

String_Node used to represent a string
Only stores the token and value
'''
# Import Token and AST
from ..tokens import Token
from .ast import AST

class String_Node(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = self.token.value