from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from pattern_ctrl import PatternInputController
from smtplib import SMTP, SMTPException
import time
import signal
import os


class WeatherApp():

	def __init__(self):
		self.sense = SenseHat()
		self.pattern_ctrl = PatternInputController(self.sense)
		
		self.sender = "diegogarcialozano95@gmail.com"
		self.pwd = "weatherapp"

		self.message = "From: From Raspberry Weather App <diegogarcialozano95@gmail.com>"
		self.message += "\nTo: To {username} <{usermail}>"
		self.message += "\nSubject: Weather App Report\n"
		self.message += "\n Hello {username1} ! Here is the weather data that was recorded:\n"
		self.message += "\n Temperature: {temp:.2f} Celsius"
		self.message += "\n Pressure: {press:.2f} Milibars"
		self.message += "\n Humidity: {humid:.2f} %"
		self.message += "\n\n Next report will be in {wait} seconds"

		while True:
			os.system("clear")
			self.sense.clear()
			print "Enter your Username and then your pattern in the Raspberry Pi"
			print "Type 'exit' to close \n"

			username = raw_input("Username: ")
			if username == "exit":
				print "\nBye!!"
				self.sense.show_message("Bye!!")
				break
			print "\nEnter your authentication pattern in the Raspberry Pi"
			print "\n  - Move the joystick to move around"
			print "\n  - Push the joystick to select/deselect"
			print "\n  - Press any place along the green lines to submit"
			pattern = self.pattern_ctrl.get_input_pattern()

			#try:
				#user_logged = self.login(username,pattern)
			self.sense.load_image("res/success.png")
			print "\nWelcome " + username + " !"
			time.sleep(2)
			self.sense.clear()
			self.record_weather() #pasar usuario
			#except Exception as e:
			#	print e
			#	self.sense.load_image("res/error.png")
			#	print "Invalid credentials"
			#	time.sleep(2)
			#	self.sense.clear()
		
	def send_mail(self,t,p,h):
		try:
			self.smtp = SMTP("smtp.gmail.com:587")
			self.smtp.ehlo()
			self.smtp.starttls()
			self.smtp.login(self.sender, self.pwd)
			self.message = self.message.format(username="Diego",
					    usermail="diegogarcialozano95@gmail.com",
					    username1="Diego",
					    temp = t,
					    press = p,
					    humid = h,
					    wait = 5)
			self.smtp.sendmail(self.sender, ["diegogarcialozano95@gmail.com"], self.message)
			self.smtp.quit()
		except SMTPException:
			print "Error: unable to send email"

	def login(self,username,pattern):
		raise Exception("Invalid credentials")

	def record_weather(self):
		wait = 30
		while True:
			temperature = self.sense.get_temperature()
			pressure = self.sense.get_humidity()
			humidity = self.sense.get_pressure()

			self.send_mail(temperature,pressure,humidity)

			for i in range (wait):
				self.animation()
			
	def animation(self):
		"One second animation"
		self.sense.load_image("res/cloud1.png")
		time.sleep(0.25)
		self.sense.load_image("res/cloud2.png")
		time.sleep(0.25)
		self.sense.load_image("res/cloud3.png")
		time.sleep(0.25)
		self.sense.load_image("res/cloud2.png")
		time.sleep(0.25)
		
if __name__ == "__main__":
	weather_app = WeatherApp()
	
