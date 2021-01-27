import curses
import time

def setup(stdscr: curses.window):
    t = 'Welcome to the test run baby'

def main(stdscr: curses.window):
    while True:
        u = stdscr.getch()
        if u == curses.KEY_UP:
            stdscr.addstr(0, 0, 'Pressed key up')
            stdscr.chgat(-1)
        elif u == curses.KEY_DOWN:
            stdscr.addstr(0, 0, 'Pressed key down')
            stdscr.chgat(-1)
        else:
            stdscr.addstr(0, 0, 'Nani what key')
            stdscr.chgat(-1)
        stdscr.noutrefresh()
        curses.doupdate()

curses.wrapper(main)