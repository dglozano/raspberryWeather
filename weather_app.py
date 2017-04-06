from matrix_ctrl import MatrixController
from persistence import Persistence
from sense_hat import SenseHat
from smtplib import SMTP, SMTPException
import signal

class WeatherAppService():

	def __init__(self):
		self.persistence = Persistence()
		self.matrix_ctrl = MatrixController()
		signal.signal(signal.SIGINT, self.sigint_handler)

		self.sender = "diegogarcialozano95@gmail.com"
		self.pwd = "weatherapp"

		while True:
			username = self.matrix_ctrl.get_username()
			if username == MatrixController.USER_EXIT:
				self.matrix_ctrl.exit()
				break
			pattern = self.matrix_ctrl.get_input_pattern()
			pattern = self.pattern_to_string(pattern)
			try:
				self.user_logged = self.persistence.login(username,pattern)
			except Exception as error:
				self.matrix_ctrl.display_error(error)
			else:
				self.matrix_ctrl.display_success(self.user_logged)
				self.record_weather()
		
	def send_mail(self,t,p,h):
		with open('res/email.txt','r') as email_file:
			message = email_file.read()

		message = message.format(
			username=self.user_logged['name'],
			usermail=self.user_logged['mail'],
			username1=self.user_logged['name'],
			temp = t,
			press = p,
			humid = h,
			wait = self.user_logged['wait']
		)

		try:
			self.smtp = SMTP("smtp.gmail.com:587")
			self.smtp.ehlo()
			self.smtp.starttls()
			self.smtp.login(self.sender, self.pwd)
			self.smtp.sendmail(self.sender, [self.user_logged['mail']], message)
			self.smtp.quit()
		except SMTPException as error:
			self.matrix_ctrl.display_error(error)

	def record_weather(self):
		self.logout = False
		while self.logout == False:
			timer = 0
			
			sense = SenseHat()
			temperature = sense.get_temperature()
			humidity = sense.get_humidity()
			pressure = sense.get_pressure()

			self.send_mail(temperature,pressure,humidity)

			while self.logout == False and timer < self.user_logged['wait']:
				self.matrix_ctrl.animation()
				timer += 1

	def sigint_handler(self, signum, frame):
		self.logout = True

	def pattern_to_string(self, pattern):
		for i in range(len(pattern)):
			pattern[i] = "Y" if pattern[i] == True else "N"
		return ''.join(pattern)

if __name__ == "__main__":
	WeatherAppService()

