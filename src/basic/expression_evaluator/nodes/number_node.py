
'''
This is the Python File containing the Child class, 'Number_Node' that inherits from AST
'''
from .ast import AST

class Number_Node(AST):
    def __init__(self, token):
        self.token = token
        self.token_value = token.token_value

    def __str__(self):
        #! Placeholder __str__() function
        return f"{self.token}"