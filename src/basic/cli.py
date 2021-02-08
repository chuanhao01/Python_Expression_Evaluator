'''
    This Python File deals with the CLI of the application

    It also contains a CLI class that will have the different necessary print statements for each section identified
'''

#* Importing Modules
import os.path
from .expression_evaluator.evaluator import Evaluator
from .expression_evaluator.compiler.node_traversal import PreOrder, InOrder, PostOrder
from ..common.expression_sorter import File, Sort


class CLI:
    #* General

    def __init__(self):
        pass

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
        print("Please select your choice <'1', '2', '3'>:")
        print("\t 1. Evaluate expression")
        print("\t 2. Sort expressions")
        print("\t 3. Exit")
        
        return input("Enter choice: ")

    @staticmethod
    def print_exit():
        print("\nBye, thanks for using ST107 DSAA: Expression Evaluator & Sorter")

    @staticmethod
    def print_continue():
        input("\nPress any key to continue....\n")


    #* Expression Evaluator

    @staticmethod
    def print_inputExpression():
        return input("Please enter the expression you want to evaluate: \n")
        
    @staticmethod
    def print_traversalSelection():
        print("\nPlease select your choice <'1', '2', '3'>:")
        print("\t 1. Pre Order Tree Traversal")
        print("\t 2. In Order Tree Traversal")
        print("\t 3. Post Order Tree Traversal")    

        choice = -1
        while choice not in ["1", "2", "3"]:
            choice = input("Enter choice: ")

        return choice

    @staticmethod
    def print_parseTree(traversalChoice, ast):
        print("\nExpression Tree:")

        if traversalChoice == "1":
            preorder = PreOrder()
            preorder.traverse(node = ast)

        elif traversalChoice == "2":
            inorder = InOrder()
            inorder.traverse(node = ast)

        elif traversalChoice == "3":
            postorder = PostOrder()
            postorder.traverse(node = ast)

    @staticmethod
    def print_evaluateResult(result):
        print("\nExpression evaluates to:")
        print(result)

    
    #* Expression Sorter

    @staticmethod
    def get_files():
        input_file = ""
        output_file = ""

        print("\nPlease enter your input and output files below..")
        while not os.path.exists(input_file):
            input_file = input("Please enter input file: ")

        while not os.path.exists(output_file):
            output_file = input("Please enter output file: ")

        return (input_file, output_file)

    @staticmethod
    def get_sortSettings():
        choice = -1

        while choice not in ['1', '2']:
            print("\nPlease enter your choice <'1', '2'>:")
            print("\t 1. Sort by Ascending")
            print("\t 2. Sort by Descending")

            choice = input("Enter choice: ")

        if choice == '1':
            sort_order = "ascending"

        else:
            sort_order = "descending"

        return sort_order

    @staticmethod
    def print_sortResult(sortedList):
        print(">>> Evaluating and Sorting started:")

        for sublist in sortedList:
            value = sublist[0]
            print(f"\n*** Expressions with value = {value}")

            for expression in sublist[1]:
                print(f"{expression[0]} ==> {value}")

        print("\n>>> Evaluating and Sorting completed!")

    
    def run(self):
        CLI.print_header()
        done = False

        while not done:
            choice = CLI.print_selectionScreen()

            if choice == '1':
                expression_evaluated = False

                # Continue trying to get a valid expression input from the user as long as there was an error raised
                while not expression_evaluated:
                    try:
                        expression = CLI.print_inputExpression()
                        traversalChoice = CLI.print_traversalSelection()
                        ast, result = Evaluator.evaluate(expression)

                        expression_evaluated = True
                    except Exception as error:
                        print(error)
                        continue

                CLI.print_parseTree(traversalChoice, ast)
                CLI.print_evaluateResult(result)

                CLI.print_continue()

            elif choice == '2':
                valid_expressions = True

                input_file, output_file = CLI.get_files()
                sort_order = CLI.get_sortSettings()
                
                allExpressions = File.read(input_file)

                # Obtain the evaluated value for each expression in the list provided
                for expression in allExpressions:
                    try:
                        expression.append(Evaluator.evaluate(expression[0])[1])
                    except Exception as error:
                        print(f"There was an invalid expression in {input_file}.. The specific error is as follows:")
                        print(error, "\n")

                        valid_expressions = False
                        break

                if valid_expressions:
                    # Sort the expressions according to value
                    # sort = Sort(all_expr_list = allExpressions, sort_type = sort_type, sort_order = sort_order)
                    sort = Sort(all_expr_list = allExpressions, sort_order = sort_order)
                    sortedList = sort.sort()

                    CLI.print_sortResult(sortedList)
                    File.write(output_file, sortedList)

                    CLI.print_continue()

            elif choice == '3':
                CLI.print_exit()
                done = True