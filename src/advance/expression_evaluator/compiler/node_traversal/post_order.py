'''Python file for the post_order traversal

This is a helper class used to generate the post-order traversal of a given ast
'''
from ...nodes import AST
from ...nodes import Number_Node, String_Node, UnaryOp_Node, BinaryOp_Node, Function_Node

from .traversal import Traversal

class PostOrderTraversal(Traversal):
    def __init__(self):
        self.__traversal = []

    # Public methods
    def traverse(self, ast: AST):
        '''
        Public method called to get the traversal graph
        '''
        self.visit(ast)
        return self.__traversal

    # Node Type Visitor Implementation
    def visit_BinaryOp_Node(self, node: BinaryOp_Node, level: int=1):
        token = node.token
        self.visit(node.left, level=level+1)
        self.visit(node.right, level=level+1)
        self.__traversal.append(f"{'>'*level}: {str(token)}")
    def visit_UnaryOp_Node(self, node: UnaryOp_Node, level: int=1):
        token = node.token
        self.visit(node.child, level=level+1)
        self.__traversal.append(f"{'>'*level}: {str(token)}")
    def visit_Function_Node(self, node: Function_Node, level: int=1):
        token = node.token
        for argument in node.arguments:
            self.visit(argument, level=level+1)
        self.__traversal.append(f"{'>'*level}: {str(token)}")
    def visit_Number_Node(self, node: Number_Node, level: int=1):
        token = node.token
        self.__traversal.append(f"{'>'*level}: {str(token)}")
    def visit_String_Node(self, node: String_Node, level: int=1):
        token = node.token
        self.__traversal.append(f"{'>'*level}: {str(token)}")