'''Advance Application CLI file

'''
import curses
import time
import curses.panel as panel

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
        self.__application_instructions = ['Please use your arrow keys to hover over the option you want to select', 'The current select will be highlighted', 'Press enter to select the option']
        self.__creator_names = ['Chuan Hao(1922264)', 'Sherisse(1935967)']
        self.__creator_class = 'DIT/FT/2B/11'
        self.__selection_options = [
            {
                'str': 'Evaluate an Expression',
                'method_name': '__update_expression'
            },
            {
                'str': 'Sort the Expression in a file',
                'method_name': 'method_2'
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
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK) # Expression
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK) # Expression Visual Pad

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
        # self.__application_terminal_window.setscrreg(0, self.__application_height - 3)
    
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
            # self.__selection_window.addstr(y, x, str(user_key))
            # self.__selection_window.addstr(y+1, x, str(curses.KEY_ENTER))
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
                # Debug
                # self.__selection_window.addstr(y, x, str(method))
                return method()
    
    def __load_exit(self):
        '''
        Helper private function to load the default state of the exit
        '''
        curses.noecho()
        curses.curs_set(0)

        self.__current_application = 'Exiting Application'

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
        # s = f"Bye. :D"
        # x = width - len(s) // 2
        # self.__exit_window.addstr(y, x, s)
        # Refresh
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
            
        return

    def __load_expression(self):
        curses.noecho()
        curses.curs_set(0)
        curses.cbreak()

        self.__current_application = 'Expression Evaluator'
        self.__current_application_attributes = curses.color_pair(2)
        self.__application_terminal_y = self.__application_terminal_window.getmaxyx()[0]
        self.__application_terminal_y -= 1
        self.__application_terminal_window.move(self.__application_terminal_y, self.__application_terminal_x)

        self.__update_application_panel(self.__application_terminal_panel)

    def __update_expression(self):
        self.__load_expression()
        self.__refresh()
        while True:
            s = "Press 'i' to start writing your expression, Press 'esc' to look at the history of your past evaluated expressions"
            self.__write_expression_visual_pad(s)
            self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, s)
            self.__application_terminal_window.scroll()

            user_key = self.__application_terminal_window.getch()
            if user_key == 27:
                # Esc key, go into pad mode
                self.__update_application_history_pad()
                # Load expression again
                self.__load_expression()
                self.__refresh()
            elif user_key in set([ord('i')]):
                # Insert mode, start writing your expression
                s = "Your Expression: "
                self.__application_terminal_window.addstr(self.__application_terminal_y, self.__application_terminal_x, s)

                curses.echo()
                curses.curs_set(1)
                expression_str = self.__application_terminal_window.getstr()
                self.__write_expression_visual_pad(f"{s}{expression_str}")
                curses.noecho()
                curses.curs_set(0)
            self.__refresh()

    
    def __write_expression_visual_pad(self, s):
        '''
        Writes the given string to the expression pad
        '''
        self.__application_history_pad.addstr(self.__history_length - 1, 0, s)
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
            if user_key in set([ord('k')]):
                # Move down
                self.__application_history_pad_pos -= 1
            elif user_key in set([ord('j')]):
                # Move up
                if self.__application_history_pad_pos < self.__history_length:
                    self.__application_history_pad_pos += 1
            elif user_key in set([ord('i')]):
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