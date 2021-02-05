'''
This Python file deals with the evaluation of expressions and,
integrates the lexer, parser and interpreter together
'''

from .compiler import Lexer, Parser, Interpreter

class Evaluator:
    @staticmethod
    def evaluate(expression):
        # Initialising the different components of the basic compiler
        lexer = Lexer(expression)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)

        # Obtaining the result
        return interpreter.interpret()