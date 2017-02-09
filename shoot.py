#!python2.7

from time import clock
import curses
import random

art = dict()

def load_art():
    artfile = open("art.txt", "r")
    artlines = []
    for line in artfile:
        artlines.append(line)

    cur_art = []
    for i in range(0, len(artlines)):
        if(artlines[i][0] == '?' and artlines[i][1] != '#'):
            j = i + 1
            while(artlines[j][0] != '?'):
                cur_art.append(artlines[j][0:len(artlines[j]) - 1])
                j += 1
            art[artlines[i][2:len(artlines[i]) - 1]] = cur_art
            cur_art = []
    print(art)

def draw_art(stdscr, key, line, col):
    for artl in art[key]:
        stdscr.addstr(line, col, artl)
        line += 1
           
def end_app(stdscr):
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()

def scrn_title(stdscr):
	draw_clr(stdscr)
	draw_art(stdscr, 'titleborder', 0, 0)
	stdscr.refresh()
	stdscr.getch()

def scrn_names(stdscr):
	draw_clr(stdscr)
	names = ["", ""]
	stdscr.addstr(5, 2, "Enter first player name: ")
	stdscr.refresh()
	cur_char = 0
	while(True):
		cur_char = stdscr.getch()
		if(cur_char == 10):
			break
		names[0] += chr(cur_char)
	stdscr.addstr(7, 2, "Enter first player name: ")
	stdscr.refresh()
	while(True):
		cur_char = stdscr.getch()
		if(cur_char == 10):
			break
		names[1] += chr(cur_char)
	stdscr.addstr(9, 2, "Names are {} and {}".format(names[0], names[1]))
	stdscr.addstr(11, 2, "Press any key to continue.")
	stdscr.getch()
	return names

def scrn_feelings(stdscr, names):
	draw_clr(stdscr)
	feelings = [random.random() * 2, random.random() * 2]
	stdscr.addstr(5, 2, "{}: {}".format(names[0], feelings[0]))
	stdscr.addstr(6, 2, "{}: {}".format(names[1], feelings[1]))
	stdscr.getch()
	return feelings

def scrn_shootout(stdscr, names, feelings):
	draw_clr(stdscr)
	draw_bg(stdscr)
	draw_playerA(stdscr, 0)
	draw_playerB(stdscr, 0)
	
	stdscr.nodelay(True)
	
	state = [0, 0]
	reach_time = [0, 0]
	
	while(True):
		cur_time = clock()
		
		if(state[0] == 1 and cur_time > feelings[0] + reach_time[0]):
			state[0] = 2
		
		if(state[1] == 1 and cur_time > feelings[1] + reach_time[1]):
			state[1] = 2
			
		draw_playerA(stdscr, state[0])
		draw_playerB(stdscr, state[1])
		
		cur = stdscr.getch()
		if(cur == curses.ERR):
			continue
			
		if(cur == ord('a')):
			# PlayerA's Control
			if(state[0] == 0):
				# Raise gun
				state[0] = 1
				reach_time[0] = cur_time
			elif(state[0] == 1):
				# Shoot ground
				stdscr.addstr(13, 7, "oops")
				state[0] = 3
			elif(state[0] == 2):
				# Shoot enemy
				stdscr.addstr(13, 7, "gotcha")
				state[0] = 3
				state[1] = 5
			elif(state[0] == 3):
				# Out of ammo, trying to shoot
				stdscr.addstr(13, 7, "i'm out...")
			elif(state[0] == 5):
				# Dead
				stdscr.addstr(13, 7, ".............")
			
		if(cur == ord('l')):
			# PlayerB's Control
			if(state[1] == 0):
				# Raise gun
				state[1] = 1
				reach_time[1] = cur_time
			elif(state[1] == 1):
				# Shoot ground
				stdscr.addstr(13, 50, "oops")
				state[1] = 3
			elif(state[1] == 2):
				# Shoot enemy
				stdscr.addstr(13, 50, "gotcha")
				state[1] = 3
				state[0] = 5
			elif(state[1] == 3):
				# Out of ammo, trying to shoot
				stdscr.addstr(13, 50, "i'm out...")
			elif(state[1] == 5):
				# Dead
				stdscr.addstr(13, 50, ".............")

		if(cur == ord('q')): break

def draw_clr(stdscr):
	for r in range(0, curses.LINES):
		for c in range(0, curses.COLS - 1):
			stdscr.addstr(r, c, ' ')

def draw_bg(stdscr):
	for c in range(0, curses.COLS - 1):
		stdscr.addstr(15, c, '_')
	stdscr.addstr(12, 30, ' | |_|')
	stdscr.addstr(13, 30, ' |_|  ')
	stdscr.addstr(14, 30, '  ||  ')
	stdscr.refresh()
	stdscr.move(0, 0)
	
def draw_playerA(stdscr, stance):
	if(stance == 0 or stance == 3):
		stdscr.addstr(14, 7, '  o  ')
		stdscr.addstr(15, 7, ' ||| ')
		stdscr.addstr(16, 7, '_/ \_')
	if(stance == 1):
		stdscr.addstr(14, 7, '  o  ')
		stdscr.addstr(15, 7, ' ||\\ ')
		stdscr.addstr(16, 7, '_/ \_')
	if(stance == 2):
		stdscr.addstr(14, 7, '  o_ ')
		stdscr.addstr(15, 7, ' ||  ')
		stdscr.addstr(16, 7, '_/ \_')
	if(stance == 5):
		stdscr.addstr(14, 7, ' _u_')
		stdscr.addstr(15, 7, '|_ _|')
		stdscr.addstr(16, 7, '\|_|/')
	stdscr.refresh()
	stdscr.move(0, 0)
	
def draw_playerB(stdscr, stance):
	if(stance == 0 or stance == 3):
		draw_art(14, 60, 'leftcowboy0')
	if(stance == 1):
		stdscr.addstr(14, 60, '  o  ')
		stdscr.addstr(15, 60, ' ||\\ ')
		stdscr.addstr(16, 60, '_/ \_')
	if(stance == 2):
		stdscr.addstr(14, 60, '  o_ ')
		stdscr.addstr(15, 60, ' ||  ')
		stdscr.addstr(16, 60, '_/ \_')
	if(stance == 5):
		stdscr.addstr(14, 60, ' _u_')
		stdscr.addstr(15, 60, '|_ _|')
		stdscr.addstr(16, 60, '\|_|/')
	stdscr.refresh()
	stdscr.move(0, 0)

start_time = clock()
load_art()
stdscr = curses.initscr()
curses.cbreak()
stdscr.leaveok(True)

scrn_title(stdscr)
names = scrn_names(stdscr)
feelings = scrn_feelings(stdscr, names)

curses.noecho()

scrn_shootout(stdscr, names, feelings)

stdscr.getch()
end_app(stdscr)