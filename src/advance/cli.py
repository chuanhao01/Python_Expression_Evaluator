'''Advance Application CLI file

'''
import curses
import time
import curses.panel as panel

# Importing evaluator
from .expression_evaluator import Evaluator

class CLI(object):
    def __init__(self):
        # Curses objs
        self.__stdscr = None
        self.__height, self.__width = None, None
        self.__history_length = 300

        self.__header_window = None
        self.__header_height, self.__header_width = None, None
        self.__header_y, self.__header_x = None, None

        # Application window
        self.__application_window = None
        self.__application_height, self.__application_width = None, None

        # Selection 
        self.__selection_panel = None
        self.__selection_window = None
        self.__selection_y, self.__selection_x = None, None

        # Expression
        self.__application_terminal_panel = None
        self.__application_terminal_window = None
        self.__application_terminal_y, self.__application_terminal_x = None, None
        # Expression visual pad
        self.__application_history_pad = None
        self.__application_history_pad_pos = None

        # Exit panel
        self.__exit_panel = None
        self.__exit_window = None
        self.__exit_y, self.__exit_x = None, None

        # Configs
        self.__application_title = ['ST107 DSAA: Expression Evaluator & Sorter', 'Advance Application']
        self.__application_instructions = [
            "For the selection menu: Use 'UP' and 'DOWN' arrow keys to navigate the menu. Press 'ENTER' to select and option",
            "For the application history: Use the 'UP' and 'DOWN' arrow keys to move through the history. Press 'ESC' to leave the history"
        ]
        self.__creator_names = ['Chuan Hao(1922264)', 'Sherisse(1935967)']
        self.__creator_class = 'DIT/FT/2B/11'
        self.__selection_options = [
            {
                'str': 'Evaluate an Expression',
                'method_name': '__update_expression_evaluator'
            },
            {
                'str': 'Sort the Expression in a file',
                'method_name': '__update_file_sorter'
            },
            {
                'str': "Look at the application's history",
                'method_name': '__update_application_history_pad'
            },
            {
                'str': 'Exit',
                'method_name': '__update_exit'
            }
        ]

        self.__current_application = None
        self.__current_application_attributes = None

        curses.wrapper(self.__main)
    
    def __error(self):
        raise Exception('Unexpected CLI error has occurred')
    
    def __set_up(self):
        '''
        Main helper function to set up everything
        Set up only includes things that will run only once
        '''
        self.__set_up_config()
        self.__set_up_windows()
        self.__set_up_windows_configs()
        self.__set_up_panels()

    def __set_up_config(self):
        '''
        Set up curses configs
        '''
        # curses.curs_set(1)
        # Setting up color pairs
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Selection highlight
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK) # Expression Evaluator
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK) # Expression File Sorter
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK) # Application History
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK) # Exit application

    def __set_up_windows(self):
        '''
        Set up other windows
        '''
        self.__height, self.__width = self.__stdscr.getmaxyx()

        # Header window
        self.__header_height, self.__header_width = int(self.__height * 0.3), self.__width
        self.__header_window = self.__stdscr.derwin(self.__header_height, self.__header_width, 0, 0)
        self.__header_y, self.__header_x = (1, 1)
        self.__header_window.move(self.__header_y, self.__header_x)

        # Application window
        self.__application_height, self.__application_width = self.__height - self.__header_height, self.__width
        self.__application_window = self.__stdscr.derwin(self.__application_height, self.__application_width, self.__header_height, 0)
        self.__application_window.box()

        # Selection window
        self.__selection_window = self.__application_window.derwin(self.__application_height - 2, self.__application_width - 2, 1, 1)
        self.__selection_y, self.__selection_x = (0, 0)
        self.__selection_window.move(self.__selection_y, self.__selection_x)

        # Expression window
        self.__application_terminal_window = self.__application_window.derwin(self.__application_height - 2, self.__application_width - 2, 1, 1)
        self.__application_terminal_y, self.__application_terminal_x = (0, 0)
        self.__application_terminal_window.move(self.__application_terminal_y, self.__application_terminal_x)

        # Expression visual pad
        self.__application_history_pad = curses.newpad(self.__history_length, self.__application_width - 2)
        self.__application_history_pad_pos = self.__history_length - 1

        # Exit window
        self.__exit_window = self.__application_window.derwin(self.__application_height - 2, self.__application_width - 2, 1, 1)
        self.__exit_y, self.__exit_x = (0, 0)
        self.__exit_window.move(self.__selection_y, self.__selection_x)
    
    def __set_up_windows_configs(self):
        # Standard Keypads
        self.__stdscr.keypad(1)
        self.__header_window.keypad(1)
        self.__application_window.keypad(1)
        self.__selection_window.keypad(1)
        self.__application_terminal_window.keypad(1)
        self.__application_history_pad.keypad(1)

        # Expression
        self.__application_terminal_window.scrollok(True)
        self.__application_history_pad.scrollok(True)
    
    def __set_up_panels(self):
        self.__selection_panel = panel.new_panel(self.__selection_window)
        self.__application_terminal_panel = panel.new_panel(self.__application_terminal_window)
        self.__exit_panel = panel.new_panel(self.__exit_window)
    
    def __refresh(self):
        self.__stdscr.noutrefresh()
        self.__header_window.noutrefresh()
        self.__application_window.noutrefresh()
        self.__selection_window.noutrefresh()
        self.__application_terminal_window.noutrefresh()
        self.__exit_window.noutrefresh()
        curses.doupdate()

    def __update_application_panel(self, top_panel=None):
        '''
        Private helper function to erase the application, set the given panel to the top and update the panels
        '''
        self.__application_window.erase()
        self.__header_window.erase()
        self.__load_header()
        self.__load_application()
        if top_panel is not None:
            top_panel.top()
            panel.update_panels()
    
    def __load_header(self):
        '''
        Private helper function for loading the header
        '''
        # Setup
        self.__header_y, self.__header_x = (1, 1)
        self.__header_window.box()
        # Calculate width for later on
        width = self.__header_width - 2
        width = width//2

        # Adding title
        for title in self.__application_title:
            x = width - len(title)//2
            self.__header_window.addstr(self.__header_y, x, title)
            self.__header_y += 1

        # Adding break
        self.__header_window.addstr(self.__header_y, self.__header_x, '-'*(self.__header_width - 2))
        self.__header_y += 1

        # Adding names
        creator_names_str = f"- Done by: {' & '.join(self.__creator_names)}"
        x = width - len(creator_names_str)//2
        self.__header_window.addstr(self.__header_y, x, creator_names_str)
        self.__header_y += 1

        # Adding class
        creator_class_str = f"- Class: {self.__creator_class}"
        x = width - len(creator_class_str)//2
        self.__header_window.addstr(self.__header_y, x, creator_class_str)
        self.__header_y += 1

        # Newline
        self.__header_y += 1
        
        # Adding instructions
        for instruction in self.__application_instructions:
            x = width - len(instruction)//2
            self.__header_window.addstr(self.__header_y, x, instruction)
            self.__header_y += 1
        
        # Adding current application
        self.__header_y += 1
        x = width - len(self.__current_application)//2
        if self.__current_application_attributes is None:
            self.__header_window.addstr(self.__header_y, x, self.__current_application)
        else:
            self.__header_window.addstr(self.__header_y, x, self.__current_application, self.__current_application_attributes)
    
    def __load_application(self):
        '''
        Helper private function to load the default state of the application
        '''
        self.__application_window.box()
    
    def __load_selection(self):
        '''
        Helper private function to load the default state of the selection
        '''
        # Curses config
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)

        # Set application config
        self.__current_application = 'Selection Menu'
        self.__current_application_attributes = curses.color_pair(1)

        # Update panel
        self.__update_application_panel(self.__selection_panel)

    def __update_selection(self):
        '''
        Update selection
        '''
        # Set up selection
        self.__load_selection()
        self.__refresh()
        current_index = 0
        while True:
            width = self.__application_width // 2
            height = self.__application_height // 2
            y = height - len(self.__selection_options)//2
            for index, option in enumerate(self.__selection_options):
                # Get string and find x, y
                option_str = f"{index + 1}. {option['str']}"
                x = width - len(option_str)//2
                if current_index == index:
                    self.__selection_window.addstr(y, x, option_str, curses.A_STANDOUT)
                else:
                    self.__selection_window.addstr(y, x, option_str)
                # Update y
                y += 1
            self.__refresh()
            user_key = self.__selection_window.getch()
            if user_key in set([curses.KEY_UP, ord('w'), ord('k')]):
                # For key up keypress
                if current_index == 0:
                    # If we are looping back
                    current_index = len(self.__selection_options) - 1
                else:
                    # If normal key press
                    current_index -= 1
            elif user_key in set([curses.KEY_DOWN, ord('s'), ord('j')]):
                if current_index == len(self.__selection_options) - 1:
                    # If we are looping back
                    current_index = 0
                else:
                    # If normal key press
                    current_index += 1
            elif user_key in set([curses.KEY_ENTER, 10, 13]):
                # When enter is pressed
                option = self.__selection_options[current_index]
                method_name = f"_{self.__class__.__name__}{option['method_name']}"
                method = getattr(self, method_name, self.__error)

                # Call the method selected
                return_code = method()

                if return_code == 1:
                    # Application should exit, exit code 1
                    return
                
                # Re-load the selection
                self.__load_selection()
                self.__refresh()

    def __load_exit(self):
        '''
        Helper private function to load the default state of the exit
        '''
        curses.noecho()
        curses.curs_set(0)

        self.__current_application = 'Exiting Application'
        self.__current_application_attributes = curses.color_pair(5)

        self.__update_application_panel(self.__exit_panel)
    
    def __update_exit(self):
        # Set up exit
        self.__load_exit()
        self.__refresh()

        # Final exit draw
        width = self.__application_width // 2
        height = self.__application_height // 2
        y = height - 2
        s = f"Thank you for using the advance application"
        x = width - len(s) // 2
        self.__exit_window.addstr(y, x, s)
        y += 1
        self.__refresh()

        # Countdown to leave
        for count in range(3, -1, -1):
            # Get string for countdown
            s = f"The application will close in {count} seconds"
            # Cal
            x = width - len(s) // 2
            # Show string
            self.__exit_window.addstr(y, x, s)
            self.__refresh()
            time.sleep(1)
        
        y += 1
        
        # Bye message
        s = f"Bye. :D"
        x = width - len(s) // 2
        self.__exit_window.addstr(y, x, s)
        self.__refresh()

        time.sleep(1)

        return 1 # Returns exit code for the program to end

    def __load_application_terminal_window(self, current_application, current_application_attribute):
        curses.noecho()
        curses.curs_set(0)
        curses.cbreak()

        self.__current_application = current_application
        self.__current_application_attributes = current_application_attribute
        self.__application_terminal_y = self.__application_terminal_window.getmaxyx()[0]
        self.__application_terminal_y -= 1
        self.__application_terminal_window.move(self.__application_terminal_y, self.__application_terminal_x)

        self.__update_application_panel(self.__application_terminal_panel)

    def __update_expression_evaluator(self):
        self.__load_application_terminal_window('Expression Evaluator', curses.color_pair(2))
        self.__refresh()

        expression_evaluator_prompt_str = "Press 'i' to start writing your expression, Press 'v' to look at the history of the application, Pression 'ESC' go back to the selectio menu"
        self.__write_expression_visual_pad(expression_evaluator_prompt_str)
        self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, expression_evaluator_prompt_str)
        self.__application_terminal_window.scroll()

        while True:
            user_key = self.__application_terminal_window.getch()
            if user_key in set([27]):
                # Esc key, Return to selection
                return
            elif user_key in set([ord('v')]):
                # v key, visual mode, Switch to looking at the history
                self.__update_application_history_pad()
                # Load expression again
                self.__load_application_terminal_window('Expression Evaluator', curses.color_pair(2))
                self.__refresh()
            elif user_key in set([ord('i')]):
                # Insert mode, user writes their expression
                expression_prompt = "Your Expression: "
                self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, expression_prompt)
                self.__refresh()

                # Setting for user input to show up
                curses.echo()
                curses.curs_set(1)
                # Get the expression typed in
                expression_raw_input = self.__application_terminal_window.getstr() # Read as bytes
                expression_input = str(expression_raw_input, "utf-8")
                self.__application_terminal_window.scroll()

                # Evaluator logic
                evaluator = Evaluator()
                evaluation = evaluator.evaluate(expression_input)

                # Write the expression line to history
                self.__write_expression_visual_pad(f"{expression_prompt}{expression_input}")

                # Get order of traversal
                order_chosen = None
                while order_chosen not in set(['1', '2']):
                    self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, 'Please select an order of traversal (Enter the number):')
                    self.__write_expression_visual_pad('Please select an order of traversal (Enter the number):')
                    self.__application_terminal_window.scroll()

                    self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, '1. Pre-Order Traversal')
                    self.__write_expression_visual_pad('1. Pre-Order Traversal')
                    self.__application_terminal_window.scroll()

                    self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, '2. Post-Order Traversal')
                    self.__write_expression_visual_pad('2. Post-Order Traversal')
                    self.__application_terminal_window.scroll()

                    self.__refresh()

                    order_prompt = "Your selection: "
                    self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, order_prompt)
                    order_raw_input = self.__application_terminal_window.getstr() # Read as bytes
                    order_input = str(order_raw_input, "utf-8")
                    order_chosen = order_input

                    self.__write_expression_visual_pad(f"{order_prompt}{order_input}")
                
                # Get traversal based on selection
                traversal = None
                if order_chosen == '1':
                    traversal = evaluator.get_traversal('pre_order')
                elif order_chosen == '2':
                    traversal = evaluator.get_traversal('post_order')

                # Show evaluatiopn and traversal tree
                evaluation_str = f"Evaluation: {expression_input} = {evaluation}"
                self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, evaluation_str)
                self.__write_expression_visual_pad(evaluation_str)
                self.__application_terminal_window.scroll()

                self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, 'Traversal: ')
                self.__write_expression_visual_pad('Traversal: ')
                self.__application_terminal_window.scroll()
                for traverse in traversal:
                    self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, traverse)
                    self.__write_expression_visual_pad(traverse)
                    self.__application_terminal_window.scroll()

                self.__refresh()

                # Process the expression and do something
                curses.noecho()
                curses.curs_set(0)
            else:
                continue
                
            self.__write_expression_visual_pad(expression_evaluator_prompt_str)
            self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, expression_evaluator_prompt_str)
            self.__application_terminal_window.scroll()

            self.__refresh()
    
    def __update_file_sorter(self):
        self.__load_application_terminal_window('File Sorter', curses.color_pair(3))
        self.__refresh()

        expression_evaluator_prompt_str = "Press 'i' to start writing the file locations, Press 'v' to look at the history of the application, Pression 'ESC' go back to the selectio menu"
        self.__write_expression_visual_pad(expression_evaluator_prompt_str)
        self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, expression_evaluator_prompt_str)
        self.__application_terminal_window.scroll()

        while True:
            user_key = self.__application_terminal_window.getch()
            if user_key in set([27]):
                # Esc key, Return to selection
                return
            elif user_key in set([ord('v')]):
                # v key, visual mode, Switch to looking at the history
                self.__update_application_history_pad()
                # Load expression again
                self.__load_application_terminal_window('File Sorter', curses.color_pair(2))
                self.__refresh()
            elif user_key in set([ord('i')]):
                # Insert mode, user writes their expression
                # Setting for user input to show up
                curses.echo()
                curses.curs_set(1)
                # Get the input folder location
                # Prompt
                input_file_location_prompt = "Input file location: "
                self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, input_file_location_prompt)
                # User input
                input_file_location_raw_input = self.__application_terminal_window.getstr() # Read as bytes
                input_file_location_input = str(input_file_location_raw_input, "utf-8")
                # Write the expression line to history
                self.__write_expression_visual_pad(f"{input_file_location_prompt}{input_file_location_input}")

                # Get the output folder location
                # Prompt
                output_file_location_prompt = "Output file location: "
                self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, output_file_location_prompt)
                # User input
                output_file_location_raw_input = self.__application_terminal_window.getstr() # Read as bytes
                output_file_location_input = str(output_file_location_raw_input, "utf-8")
                # Write the expression line to history
                self.__write_expression_visual_pad(f"{output_file_location_prompt}{output_file_location_input}")

                # Process the expression and do something
                curses.noecho()
                curses.curs_set(0)
            else:
                continue
                
            self.__write_expression_visual_pad(expression_evaluator_prompt_str)
            self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, expression_evaluator_prompt_str)
            self.__application_terminal_window.scroll()

            self.__refresh()
    
    def __write_expression_visual_pad(self, history_str):
        '''
        Writes the given string to the expression pad
        '''
        self.__application_history_pad.addstr(self.__history_length - 1, 0, history_str)
        self.__application_history_pad.scroll()

    def __load_application_hisotry_pad(self):
        # Mainly for setting curses settings
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()

        self.__current_application = f"Application History"
        self.__current_application_attributes = curses.color_pair(3)

        # Load header to update it
        self.__update_application_panel()

    def __update_application_history_pad(self):
        self.__load_application_hisotry_pad()
        self.__refresh()
        while True:
            self.__application_history_pad.refresh(self.__application_history_pad_pos - (self.__application_height - 2), 0, self.__header_height + 1, 1, self.__height - 2, self.__width - 1)
            user_key = self.__application_history_pad.getch()
            if user_key in set([curses.KEY_UP, ord('w'), ord('k')]):
                # Move down
                self.__application_history_pad_pos -= 1
            elif user_key in set([curses.KEY_DOWN, ord('s'), ord('j')]):
                # Move up
                if self.__application_history_pad_pos < self.__history_length:
                    self.__application_history_pad_pos += 1
            elif user_key in set([27, ord('i')]):
                return

    def __main(self, stdscr):
        self.__stdscr = stdscr
        self.__set_up()

        # Start the application
        # Application loop is -> Update -> Load -> Refresh -> loop
        # Refresh is handled by the Update function
        # Start the main application here
        self.__update_selection()

if __name__ == '__main__':
    cli = CLI()