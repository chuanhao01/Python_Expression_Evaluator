
'''
This is the Python File containing the Child class, 'BinaryOp_Node' that inherits from AST
'''
from .ast import AST

class BinaryOp_Node(AST):
    def __init__(self, left_term, operator, right_term):
        self.left_term = left_term
        self.operator = operator
        self.right_term = right_term

    def __str__(self):
        #TODO: Create a better __str__() function
        return f"{self.left_term}, {self.operator}, {self.right_term}"