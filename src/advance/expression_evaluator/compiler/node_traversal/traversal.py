'''Python file for the traversal abstract class

This is an abstract class inherited from the NodeVisitor class to allow to kwargs
'''
from ...nodes import AST
from ...nodes import NodeVisitor

class Traversal(NodeVisitor):
    def visit(self, node: AST, **kwargs):
        '''
        Public visit method
        The visit method implemented is used to call the respective visit method based on the node type
        It then passes the return value back
        '''
        node_name = type(node).__name__
        method_name = f"visit_{node_name}"
        vist_method = getattr(self, method_name, self.__visit_method_error)
        return vist_method(node, **kwargs)

    def __visit_method_error(self, node: AST, **kwargs):
        '''
        Private helper method
        Used to raise a NotImplementedError when the node type visit method is not implemented
        '''
        node_name = type(node).__name__
        error_msg = f"Visit method for {node_name} not implemented"
        error_msg += '\n'
        error_msg += f"Please implement the method visit_{node_name}"
        error_msg += '\n'
        error_msg += f"Did not expect kwargs, {','.join(['(' + str(k) + ',' + str(v) + ')' for k, v in kwargs.items()])}"
        raise NotImplementedError(error_msg)