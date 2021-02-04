'''
    This Python File deals with the CLI of the application

    It also contains a CLI class that will have the different necessary print statements for each section identified
'''

#* Importing Modules
from .expression_evaluator.evaluator import Evaluator
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
    def print_traversalSelection():
        print("\nPlease select your choice <'1', '2', '3'>")
        print("1. Pre Order Tree Traversal")
        print("2. In Order Tree Traversal")
        print("3. Post Order Tree Traversal")

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
    def print_parseTree(traversalChoice, ast):
        print("\n")        
        if traversalChoice == "1":
            preorder = PreOrder()
            preorder.print_output(node = ast)

        elif traversalChoice == "2":
            InOrder.print_output(node = ast)

        elif traversalChoice == "3":
            PostOrder.print_output(node = ast)

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

    
    #TODO: CHANGE THIS TO A NORMAL METHOD
    @staticmethod
    def run():
        CLI.print_header()

        choice = -1
        done = False

        while not done:
            # Reset the choice for next selection
            choice = -1

            while choice not in ['1', '2', '3']:
                choice = CLI.print_selectionScreen()

            if choice == '1':
                expression = CLI.print_inputExpression()
                #TODO: Add validation for expression that will prompt for another input if error raised in compiler

                #TODO: Get Parse Tree
                traversalChoice = -1

                while traversalChoice not in ['1', '2', '3']:
                    traversalChoice = CLI.print_traversalSelection()

                ast, result = Evaluator.evaluate(expression)
                CLI.print_parseTree(traversalChoice, ast)
                CLI.print_evaluateResult(result)


                CLI.print_continue()

            elif choice == '2':
                #TODO: Add valdiation for input, output files
                input_file, output_file = CLI.print_getFiles()
                CLI.print_sortResult()

                CLI.print_continue()

            elif choice == '3':
                CLI.print_exit()
                done = True