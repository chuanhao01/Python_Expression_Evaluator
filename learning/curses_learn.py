import curses
import time

def setup(stdscr: curses.window):
    t = 'Welcome to the test run baby'
    stdscr.addstr(0, 0, t)

def main(stdscr: curses.window):
    curses.curs_set(1)
    setup(stdscr)
    inner_window = curses.newwin(curses.LINES-1, curses.COLS-2, 1, 1)
    inner_window.box()
    i_y, i_x = inner_window.getmaxyx()
    t_box = inner_window.derwin(i_y-2, i_x-2, 1, 1)

    # inner_window.addstr(1, 1, f"i_y={i_y}, i_x={i_x}")
    # inner_window.addstr(2, 1, f"i_y={t_box.getmaxyx()[0]}, i_x={t_box.getmaxyx()[1]}")

    stdscr.noutrefresh()
    inner_window.noutrefresh()
    t_box.noutrefresh()
    curses.doupdate()
    while True:
        u = stdscr.getch()
        if u == curses.KEY_UP:
            t_box.addstr(0, 0, 'Pressed key up')
            t_box.chgat(-1)
        elif u == curses.KEY_DOWN:
            t_box.addstr(0, 0, 'Pressed key down')
            t_box.chgat(-1)
        else:
            t_box.addstr(0, 0, 'Nani what key')
            t_box.chgat(-1)

        # inner_window.addstr(0, 0, 'Nani')

        stdscr.noutrefresh()
        inner_window.noutrefresh()
        t_box.noutrefresh()
        curses.doupdate()

curses.wrapper(main)