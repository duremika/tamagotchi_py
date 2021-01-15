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
    stdscr.addstr(0, offset + 1, header)
    
    if mode == modes[0]:
        line = str(int(age)) + " years old"
    elif mode == modes[1]:
        line = "press <y> for give food"
    elif mode == modes[2]:
        line = "press <y> for give drink"
    elif mode == modes[3]:
        line = "press <y> for playing game"
    elif mode == modes[4]:
        line = "press <y> for wash"
        
    stdscr.addstr(1, offset + 1, line)
    
    textpad.rectangle(stdscr, *map(int, box))


def change_mode(_modes):
    global mode
    mode += 1
    if mode >= len(_modes):
        mode = 0


def draw(stdscr, box, lines):
    w = box[3] + box[1]
    x = w // 2 - len(lines[0]) // 2
    i = 0
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)

    for row in lines:
        j = 0
        row = row.strip()
        for ch in row:
            y = box[2] - offset // 2 - i
            if ch == 'y':    # yellow
                ch = ' '
                stdscr.attron(curses.color_pair(2))
            elif ch == 'b':  # blue
                ch = ' '
                stdscr.attron(curses.color_pair(3))
            elif ch == 'w':  # white
                ch = ' '
                stdscr.attron(curses.color_pair(1))
            elif ch == '_':
                ch = ' '
            
            stdscr.addstr(y, x + j, ch)
            stdscr.attroff(curses.color_pair(1))
            stdscr.attroff(curses.color_pair(2))
            stdscr.attroff(curses.color_pair(3))
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
    n = age * 5000
    n = int(n) % 10
    n = 3 if n < 4 else n % 2 + 1

    with open(f"sprites/baby_{n}.txt") as f:
        lines = f.readlines()
    
    lines.reverse()
    draw(stdscr, box, lines)


def update_age():
    delta = datetime.now() - start
    global age
    age = delta.seconds / (3600 * 4)
    

def main(stdscr):
    state = menu.main(stdscr)
    global start
    start = datetime.now()
    if state == CONTINUE:
        pass
    elif state == "NEW":
        state = egg
    elif state == SETTINGS:
        pass
    
    stdscr.nodelay(True)
    stdscr.timeout(500)
    
    height, width = stdscr.getmaxyx()
    box = (offset + 1, offset, height - offset, width - offset)
    
    while 1:
        key = stdscr.getch()
        need_change_mode = False
        if key == ord("q"):
            break
        elif key == ord("m"):
            need_change_mode = True
        
        update_age()
        
        if age >= 0.0004:
            state = baby
        state(stdscr, box, need_change_mode)


if __name__ == '__main__':
    curses.wrapper(main)
