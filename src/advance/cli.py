'''Advance Application CLI file

'''
import curses
import time

class CLI(object):
    def __init__(self):
        # Need to set up configs
        self.__stdscr = None
        self.__y, self.__x = None, None
        self.__header_window = None
        self.__header_y, self.__header_x = None, None
        self.__main_window = None
        self.__main_y, self.__main_x = None, None

        curses.wrapper(self.__main)
    
    def __set_up(self):
        '''
        Main helper function to set up everything
        '''
        self.__set_up_config()
        self.__set_up_windows()

    def __set_up_config(self):
        '''
        Set up curses configs
        '''
        curses.curs_set(1)

    def __set_up_windows(self):
        '''
        Set up other windows
        '''
        self.__y, self.__x = self.__stdscr.getmaxyx()
        self.__header_y, self.__header_x = int(self.__y * 0.3), self.__x
        self.__header_window = self.__stdscr.derwin(self.__header_y, self.__header_x, 0, 0)
        self.__header_window.box()
    
    def __refresh(self):
        self.__stdscr.noutrefresh()
        self.__header_window.noutrefresh()
        curses.doupdate()

    def __main(self, stdscr):
        self.__stdscr = stdscr
        self.__set_up()
        self.__refresh()
        time.sleep(3)

if __name__ == '__main__':
    cli = CLI()