'''Python Class Function_Node

Function_Node represents a function call node
Used by the reserved keywords and takes in arguments with arity
'''
# Import Token and AST
from ..tokens import Token
from .ast import AST

class Function_Node(AST):
    def __init__(self, token: Token, arguments: list):
        self.token = token
        self.arguments = arguments
        self.arity = len(self.arguments)
    
    def check_arity(self, actual_arity):
        '''
        Helper method to check if the given arity matches the arity of the function
        Used to check runtime(interpretation) errors
        '''
        return self.arity == actual_arity

