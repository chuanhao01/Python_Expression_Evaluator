import curses
import time

stdscr = curses.initscr()

# Setup scr
curses.noecho()
curses.curs_set(0)
curses.cbreak()

if curses.has_colors():
    curses.start_color()

# Main things happen
# text = 'a' * (curses.COLS - 1) + 'b'
# text1 = 'a' * (curses.COLS) + 'b'
# stdscr.addstr(10, 0, text)
# stdscr.addstr(11, 0, text1, curses.A_REVERSE)

# Colors
curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)

t = 'Hello world'
# stdscr.addstr(5, 5, t, curses.A_REVERSE | curses.color_pair(1))
stdscr.addstr(5, 5, t, curses.color_pair(1))


stdscr.refresh()
time.sleep(3)

# Tear down
curses.echo()
curses.curs_set(1)
curses.nocbreak()

curses.endwin()