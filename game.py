# py Desktop\python_learn\tamagotchi_py\game.py
import curses
from datetime import datetime
from curses import textpad

import menu

offset = 3
CONTINUE = "CONTINUE"
SETTINGS = "SETTINGS"

age = 0

header = "press <q> for exit, <m> for change mode"
modes = ['time', 'eat', 'drink', 'play', 'wash']
mode = 0

def print_background(stdscr, box, mode):
    stdscr.clear()
    stdscr.addstr(0, offset+1, header)


    if mode == modes[0]:
        line = str(age) + " years old"
    elif mode == modes[1]:
        line = "press <y> for give food"
    stdscr.addstr(1, offset+1, line)

    textpad.rectangle(stdscr, *map(int, box))


def change_mode(_modes):
    global mode
    mode += 1
    if mode >= len(_modes):
        mode = 0


def draw(stdscr,box, lines):
    w = box[3] + box[1]
    x = w // 2 - len(lines[0]) // 2
    i = 0
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    for row in lines:
        j = 0
        row = row.strip()
        for ch in row:
            y = box[2] - offset // 2 - i
            if ch == '_':
                ch = ' '
            elif ch == '+':
                ch = '.'
            else:
                stdscr.attron(curses.color_pair(1))
                ch = '#'

            stdscr.addstr(y, x+j, ch)
            stdscr.attroff(curses.color_pair(1))
            j += 1
        i += 1


def egg(stdscr, box, need_change_mode):
    _modes = modes[:1]
    if need_change_mode:
        change_mode(_modes)

    print_background(stdscr, box, _modes[mode])

    with open("sprites/egg.txt") as f:
        lines = f.readlines()

    lines.reverse()
    draw(stdscr, box, lines)

def baby(stdscr, box, need_change_mode):
    _modes = modes[:5]
    if need_change_mode:
        change_mode(_modes)

    print_background(stdscr, box, _modes[mode])

    with open("sprites/baby_1.txt") as f:
        lines = f.readlines()

    lines.reverse()
    draw(stdscr, box, lines)


def update_age():
    delta = datetime.now() - start
    global age
    age = delta.seconds // 3 #(3600 * 8)


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
        need_change_mode = False
        if key == ord("q"):
            break
        elif key == ord("m"):
            need_change_mode = True

        update_age()
        if age == 1:
            state = baby

        state(stdscr, box,  need_change_mode)


if __name__ == '__main__':
    curses.wrapper(main)
