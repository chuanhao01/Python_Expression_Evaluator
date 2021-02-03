'''
    This Python File deals with the CLI of the application
'''

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
        print("Bye, thanks for using ST107 DSAA: Expression Evaluator & Sorter")

    @staticmethod
    def print_continue():
        print("\n Press any key to continue....")
        input()


    #* Expression Evaluator

    @staticmethod
    def print_inputExpression():
        return input("Please enter the expression you want to evaluate: \n")

    @staticmethod
    def print_evaluateResult(expression):
        print("PRINT THE AST")

        print("Expression evaluates to:")

        #! Change this to evaluating using the parse tree
        print(eval(expression))

    
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

    
if __name__ == "__main__":
    CLI.print_header()
    
    choice = -1
    done = False

    while not done:
        # Reset the choice for next selection
        choice = -1

        while choice not in ['1', '2', '3']:
            choice = CLI.print_selectionScreen()

        if choice == '1':
            #TODO: Add validation for expression that will prompt for another input if error raised in compiler
            expression = CLI.print_inputExpression()
            CLI.print_evaluateResult(expression)

            CLI.print_continue()

        if choice == '2':
            #TODO: Add valdiation for input, output files
            input_file, output_file = CLI.print_getFiles()
            CLI.print_sortResult()

            CLI.print_continue()

        if choice == '3':
            CLI.print_exit()
            done = True

        