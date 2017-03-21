from sense_hat import ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import time

class PatternInputController():

	WHITE = [255,255,255]
	BLACK = [0,0,0]
	RED = [255,0,0]
	
	def __init__(self, sense):
		self.trying = False
		self.sense = sense
		self.handler = { "up": self.pushed_up,
			 	 "down": self.pushed_down,
				 "right": self.pushed_right,
				 "left": self.pushed_left,
				 "middle": self.pushed }
		
	def get_input_pattern(self):
		self.trying = True
		self.sense.load_image("res/start_pattern.png")
		self.x, self.y = [3, 3]
		self.next_x, self.next_y = [3, 3]
		self.hold_color = PatternInputController.BLACK
		while self.trying:
			event = self.sense.stick.wait_for_event(emptybuffer=True)
			self.handler[event.direction](event)
			self.refresh()
			if self.trying  == False:
				pattern_entered = self.sense.get_pixels()
				del pattern_entered[56:] # Delete last row
				del pattern_entered[7::8] # Delete last coloumn
				for i in range(len(pattern_entered)):
					pattern_entered[i] = pattern_entered[i] != PatternInputController.BLACK
		self.sense.clear()
		return pattern_entered

	def clamp(self,value, min_value=0, max_value=7):
		"check it doesn't go out of the boundaries of the matrix"
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
		if self.hold_color == PatternInputController.BLACK:
			self.hold_color = PatternInputController.RED
		else:
			self.hold_color = PatternInputController.BLACK

	def refresh(self):
		#Color the current pixel with the proper color before moving
		self.sense.set_pixel(self.x,self.y,self.hold_color)
		#Saves the color of the next pixel
		self.hold_color = self.sense.get_pixel(self.next_x,self.next_y)
		#Moves to the next pixel, coloring it white
		self.sense.set_pixel(self.next_x,self.next_y,PatternInputController.WHITE)
		#Updates the current position
		self.x, self.y = self.next_x, self.next_y
