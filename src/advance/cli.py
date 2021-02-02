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

        self.__selection_panel = None
        self.__selection_window = None
        self.__selection_height, self.__selection_width = None, None
        self.__selection_y, self.__selection_x = None, None

        # Configs
        self.__application_title = ['ST107 DSAA: Expression Evaluator & Sorter', 'Advance Application']
        self.__application_instructions = ['Please use your arrow keys to hover over the option you want to select', 'The current select will be highlighted', 'Press enter to select the option']
        self.__creator_names = ['Chuan Hao(1922264)', 'Sherisse(1935967)']
        self.__creator_class = 'DIT/FT/2B/11'

        self.__selection_options = ['Option 1', 'Option 2', 'Option 3']

        curses.wrapper(self.__main)
    
    def __set_up(self):
        '''
        Main helper function to set up everheightthing
        '''
        self.__set_up_config()
        self.__set_up_windows()
        self.__set_up_windows_configs()
        # self.__set_up_panels()

        # Drawing inital
        self.__load_header()

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

        self.__header_height, self.__header_width = int(self.__height * 0.3), self.__width
        self.__header_window = self.__stdscr.derwin(self.__header_height, self.__header_width, 0, 0)
        self.__header_window.box()
        self.__header_y, self.__header_x = (1, 1)
        self.__header_window.move(self.__header_y, self.__header_x)

        self.__selection_height, self.__selection_width = self.__height - self.__header_height, self.__width
        self.__selection_window = self.__stdscr.derwin(self.__selection_height, self.__selection_width, self.__header_height, 0)
        self.__selection_window.box()
        self.__selection_y, self.__selection_x = (1, 1)
        self.__selection_window.move(self.__selection_y, self.__selection_x)
    
    def __set_up_windows_configs(self):
        self.__stdscr.keypad(1)
        self.__header_window.keypad(1)
        self.__selection_window.keypad(1)
    
    def __set_up_panels(self):
        self.__selection_panel = panel.new_panel(self.__selection_window)
    
    def __refresh(self):
        self.__stdscr.noutrefresh()
        self.__header_window.noutrefresh()
        self.__selection_window.noutrefresh()
        curses.doupdate()
    
    def __load_header(self):
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

    def __update_selection(self):
        '''
        Update selection
        '''
        # Set up selection
        current_index = 0
        while True:
            width = self.__selection_width // 2
            height = self.__selection_height // 2
            y = height - len(self.__selection_options)//2
            for index, option in enumerate(self.__selection_options):
                # Get string and find x, y
                option_str = f"{index + 1}. {option}"
                x = width - len(option_str)//2
                if current_index == index:
                    self.__selection_window.addstr(y, x, option_str, curses.A_STANDOUT)
                else:
                    self.__selection_window.addstr(y, x, option_str)
                # Update y
                y += 1
            self.__refresh()
            user_key = self.__selection_window.getch()
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
                    current_index += 1
            

    def __main(self, stdscr):
        self.__stdscr = stdscr
        self.__set_up()
        self.__refresh()

        self.__update_selection()

        time.sleep(3)

if __name__ == '__main__':
    cli = CLI()