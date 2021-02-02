'''Advance Application CLI file

'''
import curses
import time
import curses.panel as panel

class OrderedDict(object):
    def __init__(self, kv_pairs=None):
        self.order = []
        self.values = {}
        self.index = 0
        if kv_pairs is not None:
            for (k, v) in kv_pairs:
                self.__setitem__(k, v)
    
    def __len__(self):
        return len(self.order)
    
    def __setitem__(self, key, value):
        self.values[key] = value
        if key not in self.values:
            self.order.append(key)
    
    def __getitem__(self, key):
        return self.values.get(key, None)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index == len(self.order):
            raise StopIteration
        self.index += 1
        return self.order[self.index], self.values[self.index]

class CLI(object):
    def __init__(self):
        # Curses objs
        self.__stdscr = None
        self.__height, self.__width = None, None

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
                'method_name': 'method_1'
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

        curses.wrapper(self.__main)
    
    def __error(self):
        raise Exception('Unexpected CLI error has occurred')
    
    def __set_up(self):
        '''
        Main helper function to set up everheightthing
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
        # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # Selection highlight

    def __set_up_windows(self):
        '''
        Set up other windows
        '''
        self.__height, self.__width = self.__stdscr.getmaxyx()

        # Header window
        self.__header_height, self.__header_width = int(self.__height * 0.3), self.__width
        self.__header_window = self.__stdscr.derwin(self.__header_height, self.__header_width, 0, 0)
        self.__header_window.box()
        self.__header_y, self.__header_x = (1, 1)
        self.__header_window.move(self.__header_y, self.__header_x)

        # Application window
        self.__application_height, self.__application_width = self.__height - self.__header_height, self.__width
        self.__application_window = self.__stdscr.derwin(self.__application_height, self.__application_width, self.__header_height, 0)
        self.__application_window.box()

        # Selection window
        self.__selection_window = self.__application_window.derwin(0, 0)
        # self.__selection_window.box()
        self.__selection_y, self.__selection_x = (1, 1)
        self.__selection_window.move(self.__selection_y, self.__selection_x)

        # Exit window
        self.__exit_window = self.__application_window.derwin(0, 0)
        # self.__exit_window.box()
        self.__exit_y, self.__exit_x = (1, 1)
        self.__exit_window.move(self.__selection_y, self.__selection_x)
        # self.__exit_window.addstr('asljdnalsdsa')
    
    def __set_up_windows_configs(self):
        self.__stdscr.keypad(1)
        self.__header_window.keypad(1)
        self.__selection_window.keypad(1)
    
    def __set_up_panels(self):
        self.__selection_panel = panel.new_panel(self.__selection_window)
        self.__exit_panel = panel.new_panel(self.__exit_window)
    
    def __refresh(self):
        self.__stdscr.noutrefresh()
        self.__header_window.noutrefresh()
        self.__selection_window.noutrefresh()
        curses.doupdate()
    
    def __load_header(self):
        '''
        Private helper function for loading the header
        '''
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
    
    def __update_header(self):
        '''
        Special update function for header
        Since the header is only loaded once, no need for loop
        '''
        self.__load_header()
        self.__refresh()
    
    def __load_application(self):
        '''
        Helper private function to load the default state of the application
        '''
        self.__application_window.box()
    
    def __update_application_panel(self, top_panel):
        '''
        Private helper function to erase the application, set the given panel to the top and update the panels
        '''
        self.__application_window.erase()
        self.__load_application()
        top_panel.top()
        panel.update_panels()

    def __load_selection(self):
        '''
        Helper private function to load the default state of the selection
        '''
        curses.cbreak()
        curses.noecho()
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
            if user_key in set([curses.KEY_UP, ord('w')]):
                # For key up keypress
                if current_index == 0:
                    # If we are looping back
                    current_index = len(self.__selection_options) - 1
                else:
                    # If normal key press
                    current_index -= 1
            elif user_key in set([curses.KEY_DOWN, ord('s')]):
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
                method()
                return
    
    def __load_exit(self):
        '''
        Helper private function to load the default state of the exit
        '''
        self.__update_application_panel(self.__exit_panel)
    
    def __update_exit(self):
        # Set up exit
        self.__load_exit()
        self.__refresh()

        # Stop the application
        time.sleep(3)
        return

    def __main(self, stdscr):
        self.__stdscr = stdscr
        self.__set_up()

        # Update header, is not part of application so its just to show
        self.__update_header()

        # Start the application
        # Application loop is -> Update -> Load -> Refresh -> loop
        # Refresh is handled by the Update function
        # Start the main application here
        self.__update_selection()

if __name__ == '__main__':
    cli = CLI()