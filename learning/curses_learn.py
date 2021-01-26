import curses
import time

def main(stdscr):
    curses.curs_set(0)
    stdscr.addstr(5, 5, "Hellow world")
    stdscr.refresh()
    time.sleep(3)
    

curses.wrapper(main)