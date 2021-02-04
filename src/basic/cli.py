'''
    This Python File deals with the CLI of the application

    It also contains a CLI class that will have the different necessary print statements for each section identified
'''

from .expression_evaluator.compiler import Lexer, Parser, Interpreter
from .expression_evaluator.compiler.node_traversal import PreOrder, InOrder, PostOrder
from ..common.expression_sorter import File, Sort

class CLI:
    #* General

    @staticmethod
    def print_header():
        print("*" * 60)
        print(f"* ST107 DSAA: Expression Evaluator & Sorter                *")
        print(f"*{'-' * 58}*")
        print(f"*{' ' * 58}*")
        print("* - Done by: Chuan Hao (1922261) & Sherisse Tan (1935967)  *")
        print("* - Class: DIT/2B/11                                       *")
        print("*" * 60)

    @staticmethod
    def print_selectionScreen():
        print("Please select your choice <'1', '2', '3'>")
        print("\t 1. Evaluate expression")
        print("\t 2. Sort expressions")
        print("\t 3. Exit")
        
        return input("Enter choice: ")

    @staticmethod
    def print_exit():
        print("\n Bye, thanks for using ST107 DSAA: Expression Evaluator & Sorter")

    @staticmethod
    def print_continue():
        print("\n Press any key to continue....")
        input()


    #* Expression Evaluator

    @staticmethod
    def print_inputExpression():
        return input("Please enter the expression you want to evaluate: \n")

    @staticmethod
    def print_evaluateResult(result):
        print("\n Expression evaluates to:")
        print(result)

    
    #* Expression Sorter

    @staticmethod
    def print_getFiles():
        input_file = input("Please enter input file: ")
        output_file = input("Please enter output file: ")

        return (input_file, output_file)

    @staticmethod
    def print_sortResult():
        print(">>> Evaluating and Sorting started:")

        print("RESULT HERE")
 
        print(">>> Evaluating and Sorting completed!")