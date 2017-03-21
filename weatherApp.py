from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import *
import sys
import time
import smtplib

class WeatherApp():

	def __init__(self):
		self.sense = SenseHat()
		self.smtp = smtplib.SMTP('localhost')
		self.smtp.sendmail('fakeuser@fake.com',['diegogarcialozano95@gmail.com'],"""hello""")
		self.users = []
		
if __name__ == "__main__":
	weather_app = WeatherApp()
	
