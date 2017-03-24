from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import time
import os

class MatrixController():

	WHITE = [255,255,255]
	BLACK = [0,0,0]
	RED = [255,0,0]
	USER_EXIT = 'exit'	

	def __init__(self):
		self.trying = False
		self.sense = SenseHat()
		self.handler = { "up": self.pushed_up,
			 	 "down": self.pushed_down,
				 "right": self.pushed_right,
				 "left": self.pushed_left,
				 "middle": self.pushed }

	def get_username(self):
		os.system("clear")
		self.sense.clear()
		print "Enter your Username. Type 'exit' to close the app \n"
		return raw_input("Username: ")
		
	def get_input_pattern(self):
		print "\nEnter your authentication pattern in the Raspberry Pi"
		print "\n	- Move the joystick to move around"
		print "\n	- Press the joystick to select/deselect"
		print "\n	- Select any spot in the green lines to submit"
		self.trying = True
		self.sense.load_image("res/start_pattern.png")
		self.x, self.y = [3, 3]
		self.next_x, self.next_y = [3, 3]
		self.hold_color = MatrixController.BLACK
		while self.trying:
			event = self.sense.stick.wait_for_event(emptybuffer=True)
			self.handler[event.direction](event)
			self.refresh()
			if self.trying  == False:
				pattern_entered = self.sense.get_pixels()
				del pattern_entered[56:] # Delete last row
				del pattern_entered[7::8] # Delete last coloumn
				for i in range(len(pattern_entered)):
					pattern_entered[i] = pattern_entered[i] != MatrixController.BLACK
		self.sense.clear()
		return pattern_entered

	def exit(self):
		print "\nBye!!"
		self.sense.show_message("Bye!!")

	def display_error(self, error):
		self.sense.load_image("res/error.png")
		print "\nAn error has occured: \n"
		print error
		print "\nPress Enter to continue"
		raw_input()
		self.sense.clear()

	def display_success(self, user):
		self.sense.load_image("res/success.png")
		print "\n\n Welcome " + user['name'] + "!"
		print "\n We will send you an email to <" + user['mail'] + "> every " + str(user['wait']) + " seconds with the weather data."
		print "\n Press Ctrl + C to logout"
		time.sleep(1)
		self.sense.clear() 
	
	def animation(self):
		"One second animation"
		self.sense.load_image("res/cloud1.png")
		time.sleep(0.25)
		self.sense.load_image("res/cloud2.png")
		time.sleep(0.25)
		self.sense.load_image("res/cloud3.png")
		time.sleep(0.25)
		self.sense.load_image("res/cloud4.png")
		time.sleep(0.25)

	def clamp(self,value, min_value=0, max_value=7):
		"Check it doesn't go out of the boundaries of the matrix"
		return min(max_value, max(min_value, value))

	def pushed_up(self,event):
		if event.action != ACTION_RELEASED:
			self.next_y = self.clamp(self.y - 1)

	def pushed_down(self,event):
		if event.action != ACTION_RELEASED:
			self.next_y = self.clamp(self.y + 1)

	def pushed_left(self,event):
		if event.action != ACTION_RELEASED:
			self.next_x = self.clamp(self.x - 1)

	def pushed_right(self,event):
		if event.action != ACTION_RELEASED:
			self.next_x = self.clamp(self.x + 1)

	def pushed(self,event):
		if event.action != ACTION_RELEASED:
			if self.x == 7 or self.y == 7:
				self.trying = False
			else:
				self.toggle_color()

	def toggle_color(self):
		"If the joystick is pressed, change the color from Black to Red or viceversa"
		if self.hold_color == MatrixController.BLACK:
			self.hold_color = MatrixController.RED
		else:
			self.hold_color = MatrixController.BLACK

	def refresh(self):
		#Color the current pixel with the proper color before moving
		self.sense.set_pixel(self.x,self.y,self.hold_color)
		#Saves the color of the next pixel
		self.hold_color = self.sense.get_pixel(self.next_x,self.next_y)
		#Moves to the next pixel, coloring it white
		self.sense.set_pixel(self.next_x,self.next_y,MatrixController.WHITE)
		#Updates the current position
		self.x, self.y = self.next_x, self.next_y
