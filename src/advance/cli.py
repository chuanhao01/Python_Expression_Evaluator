'''Advance Application CLI file

'''
import curses
import time

class CLI(object):
    def __init__(self):
        # Curses objs
        self.__stdscr = None
        self.__height, self.__width = None, None

        self.__header_window = None
        self.__header_height, self.__header_width = None, None
        self.__header_y, self.__header_x = None, None

        self.__main_window = None
        self.__main_height, self.__main_width = None, None
        self.__main_y, self.__main_x = None, None

        # Configs
        self.__application_title = ['ST107 DSAA: Expression Evaluator & Sorter', 'Advance Application']
        self.__creator_names = ['Chuan Hao(1922264)', 'Sherisse(1935967)']
        self.__creator_class = 'DIT/FT/2B/11'

        curses.wrapper(self.__main)
    
    def __set_up(self):
        '''
        Main helper function to set up everheightthing
        '''
        self.__set_up_config()
        self.__set_up_windows()

    def __set_up_config(self):
        '''
        Set up curses configs
        '''
        # curses.curs_set(1)

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

        self.__main_height, self.__main_width = self.__height - self.__header_height, self.__width
        self.__main_window = self.__stdscr.derwin(self.__main_height, self.__main_width, self.__header_height, 0)
        self.__main_window.box()
        self.__main_y, self.__main_x = (1, 1)
        self.__main_window.move(self.__main_y, self.__main_x)
    
    def __refresh(self):
        self.__stdscr.noutrefresh()
        self.__header_window.noutrefresh()
        curses.doupdate()
    
    def __update_header(self):
        # Calculate width for later on
        width = self.__header_width - 2
        width = width//2

        # Adding title
        for title in self.__application_title:
            width = self.__header_width - 2
            width = width//2
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

    def __main(self, stdscr):
        self.__stdscr = stdscr
        self.__set_up()
        self.__refresh()

        # Drawing the inital header
        self.__update_header()
        self.__refresh()

        time.sleep(3)

if __name__ == '__main__':
    cli = CLI()