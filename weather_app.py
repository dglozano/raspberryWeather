from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from pattern_ctrl import PatternInputController
from smtplib import SMTP, SMTPException

class WeatherApp():

	def __init__(self):
		self.sense = SenseHat()
		self.user_logged = "diegogarcialozano95@gmail.com"
		self.sender = "diegogarcialozano95@gmail.com"
		self.pwd = "weatherapp"
		message = """From: From Person <from@fromdomain.com>
				To: To Person <to@todomain.com>
				Subject: SMTP email test
				
				This is a test email message
				"""
		self.pattern_ctrl = PatternInputController(self.sense)
		self.username = raw_input("Username: ")
		self.pattern = self.pattern_ctrl.get_input_pattern()
		print self.pattern
		self.send_mail(message)
		
	def send_mail(self,message):
		try:
			self.smtp = SMTP("smtp.gmail.com:587")
			self.smtp.ehlo()
			self.smtp.starttls()
			self.smtp.login(self.sender, self.pwd)
			self.smtp.sendmail(self.sender, [self.user_logged], message)
			self.smtp.quit()
		except SMTPException:
			print "Error: unable to send email"
		
if __name__ == "__main__":
	weather_app = WeatherApp()
	
