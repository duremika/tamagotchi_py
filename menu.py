import curses
from game import CONTINUE, SETTINGS

buttons = ['NEW', CONTINUE, SETTINGS, 'EXIT']


def print_menu(stdscr, selected_row_idx):
	stdscr.clear()
	h, w = stdscr.getmaxyx()
	for idx, row in enumerate(buttons):
		x = w // 2 - len(row) // 2
		y = h // 2 - len(buttons) // 2 + idx
		if idx == selected_row_idx:
			stdscr.attron(curses.color_pair(1))
			stdscr.addstr(y, x, row)
			stdscr.attroff(curses.color_pair(1))
		else:
			stdscr.addstr(y, x, row)
	stdscr.refresh()


def main(stdscr):
	curses.curs_set(0)
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	current_row = 0
	print_menu(stdscr, current_row)
	
	while 1:
		key = stdscr.getch()
		
		if key == curses.KEY_UP and current_row > 0:
			current_row -= 1
		elif key == curses.KEY_DOWN and current_row < len(buttons)-1:
			current_row += 1
		elif key == curses.KEY_ENTER or key in [10, 13]:
			if current_row == len(buttons) - 1:
				exit(0)
			else:
				return buttons[current_row]
		
		print_menu(stdscr, current_row)
