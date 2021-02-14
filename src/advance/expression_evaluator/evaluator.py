'''Python file for the expression evaluataor

The expression evaluator is a wrapper class for the compiler, wrapping all the functionality into a single class and method
'''
from .compiler import Lexer, Parser, Interpreter
from .compiler.node_traversal import PreOrderTraversal, PostOrderTraversal

class Evaluator(object):
    def __init__(self):
        self.__tokens = None
        self.__ast = None

    # Main public methods
    def evaluate(self, input_expression):
        '''
        Public method used to call an evaluation for an expression
        Populates the instances __tokens and __ast
        '''
        lexer = Lexer(input_expression)
        self.__tokens = lexer.get_tokens()
        parser = Parser(self.__tokens)
        self.__ast = parser.get_ast()
        interpreter = Interpreter(self.__ast)
        evaluation = interpreter.get_interpretation()
        return evaluation
    
    def get_traversal(self, type):
        if type == 'pre_order':
            traversal = PreOrderTraversal()
            return traversal.traverse(self.__ast)
        if type == 'post_order':
            traversal = PostOrderTraversal()
            return traversal.traverse(self.__ast)
    
        