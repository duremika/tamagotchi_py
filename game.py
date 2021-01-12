# py Desktop\python_learn\tamagotchi_py\game.py
import curses
from curses import textpad

import menu

offset = 2
CONTINUE = "CONTINUE"
SETTINGS = "SETTINGS"

header = "press 'q' for exit"


def print_background(stdscr, box):
	stdscr.clear()
	stdscr.addstr(0, 4, header)
	textpad.rectangle(stdscr, *map(int, box))


def egg(stdscr, box):
	with open("sprites/egg.txt") as f:
		lines = f.readlines()
	
	height = box[3] + box[1]
	x = height // 2 - len(lines[0]) // 2
	for i, row in lines:
		for j, ch in row:
			y = box[2] - 2 - i
			if ch == '_':
				ch = ' '

			stdscr.addstr(y, x+j, ch)


def idle(stdscr, box):
	pass


def main(stdscr):
	state = menu.main(stdscr)
	
	if state == CONTINUE:
		pass
	elif state == SETTINGS:
		pass
	
	stdscr.nodelay(True)
	stdscr.timeout(100)
	
	height, width = stdscr.getmaxyx()
	box = (offset+1, offset, height - offset, width - offset)
	state = egg
	
	while 1:
		key = stdscr.getch()
		if key == ord("q"):
			break
		
		print_background(stdscr, box)
		state(stdscr, box)


if __name__ == '__main__':
	curses.wrapper(main)