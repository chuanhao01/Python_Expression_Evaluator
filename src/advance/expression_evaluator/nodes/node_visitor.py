'''Python file for NodeVisitor Class

The NodeVisitor Class is an abstract class meant to be inherited by the compiler's interpreter
It is also used to create the traversal classes
'''
# Import AST
from .ast import AST

class NodeVisitor(object):
    def visit(self, node: AST):
        '''
        Public visit method
        The visit method implemented is used to call the respective visit method based on the node type
        It then passes the return value back
        '''
        node_name = type(node).__name__
        method_name = f"visit_{node_name}"
        vist_method = getattr(self, method_name, self.__visit_method_error)
        return vist_method(node)
    
    def __visit_method_error(self, node: AST):
        '''
        Private helper method
        Used to raise a NotImplementedError when the node type visit method is not implemented
        '''
        node_name = type(node).__name__
        error_msg = f"Visit method for {node_name} not implemented"
        error_msg += '\n'
        error_msg += f"Please implement the method visit_{node_name}"
        raise NotImplementedError(error_msg)