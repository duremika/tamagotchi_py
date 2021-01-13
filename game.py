# py Desktop\python_learn\tamagotchi_py\game.py
import curses
from datetime import datetime
from curses import textpad

import menu

offset = 3
CONTINUE = "CONTINUE"
SETTINGS = "SETTINGS"

header = "press 'q' for exit"
start = None

def print_background(stdscr, box):
    stdscr.clear()
    stdscr.addstr(0, offset+1, header)
    age = datetime.now() - start
    age = age.seconds
    stdscr.addstr(1, offset+1, str(age))
    textpad.rectangle(stdscr, *map(int, box))


def egg(stdscr, box):
    with open("sprites/egg.txt") as f:
        lines = f.readlines()

    w = box[3] + box[1]
    x = w // 2 - len(lines[0]) // 2
    lines.reverse()
    i = 0
    for row in lines:
        j = 0
        row = row.strip()
        for ch in row:
            y = box[2] - offset // 2 - i
            if ch == '_':
                ch = ' '
            else:
                ch = '*'

            stdscr.addstr(y, x+j, ch)
            j += 1
        i += 1

def idle(stdscr, box):
    pass


def main(stdscr):
    state = menu.main(stdscr)

    global start
    start = datetime.now()

    if state == CONTINUE:
        pass
    elif state == SETTINGS:
        pass

    stdscr.nodelay(True)
    stdscr.timeout(500)

    height, width = stdscr.getmaxyx()
    box = (offset+1, offset, height - offset, width - offset)
    state = egg

    while 1:
        key = stdscr.getch()
        if key == ord("q"):
            break

        print_background(stdscr, box)
        state(stdscr, box)
        #stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)
