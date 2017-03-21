from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import *
import sys
import time

x = 3
y = 3
nextX = 3
nextY = 3
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
MAX_ATTEMPTS = 3
holdColor = BLACK
trying = True
sense = SenseHat()

patternDiego = [RED]
patternDiego.extend([BLACK]*48)
patternPavan = [BLACK]*48
patternPavan.append(RED)

usernames = ["dglozano", "pavan"]
patterns = [patternDiego, patternPavan]

def main(argv):
	global trying
	attempts = 0
	user_found = False
	while user_found == False and attempts < MAX_ATTEMPTS:
		username_input = raw_input("Username: ")
		try:
			user_index = usernames.index(username_input)
			user_found = True
		except:
			attempts += 1
	init_sense()
	sense.load_image("start_pattern.png")
	attempts = 0
	if user_found == True:
		print("Please, enter your pattern in the LED Matrix")
		while trying and attempts < MAX_ATTEMPTS:
			time.sleep(1)
			valid = True
			if trying  == False:
				pattern_entered = sense.get_pixels()
				del pattern_entered[56:] # Delete last row
				del pattern_entered[7::8] # Delete last coloumn
				for i in range(len(pattern_entered)):
					if pattern_entered[i] == BLACK and patterns[user_index][i] != BLACK:
						valid = False
					if patterns[user_index][i] == BLACK and pattern_entered[i] != BLACK:
						valid = False
				if valid == False:
					attempts += 1
					print("Incorrect pattern, you have %i attempt/s left" % (MAX_ATTEMPTS - attempts))
					trying = True
	else:
		print("user not found")
	if attempts < MAX_ATTEMPTS:
		print("success pattern")
	else:
		print("error pattern")			

def clamp(value, min_value=0, max_value=7):
	return min(max_value, max(min_value, value))

def pushed_up(event):
	global nextY
	if event.action != ACTION_RELEASED:
		nextY = clamp(y - 1)

def pushed_down(event):
	global nextY
	if event.action != ACTION_RELEASED:
		nextY = clamp(y + 1)

def pushed_left(event):
	global nextX
	if event.action != ACTION_RELEASED:
		nextX = clamp(x - 1)

def pushed_right(event):
	global nextX
	if event.action != ACTION_RELEASED:
		nextX = clamp(x + 1)

def direction_middle(event):
	global trying
	if event.action != ACTION_RELEASED:
		if x == 7 or y == 7:
			trying = False
		else:
			toggle(x,y)

def toggle(x,y):
	global holdColor
	if holdColor == BLACK:
		holdColor = RED
	else:
		holdColor = BLACK

def refresh():
	global x,y,nextX,nextY,holdColor
	sense.set_pixel(x,y,holdColor)
	holdColor = sense.get_pixel(nextX,nextY)
	sense.set_pixel(nextX, nextY, WHITE)
	x, y = nextX, nextY

def init_sense():
	sense.stick.direction_up = pushed_up
	sense.stick.direction_down = pushed_down
	sense.stick.direction_left = pushed_left
	sense.stick.direction_right = pushed_right
	sense.stick.direction_middle = direction_middle
	sense.stick.direction_any = refresh
	refresh()

if __name__ == "__main__":
	main(sys.argv)
