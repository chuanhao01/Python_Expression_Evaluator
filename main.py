
from src.basic.cli import CLI

#! Just having the basic application only - add advanced later
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