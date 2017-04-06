import mysql.connector
from mysql.connector import errorcode

class Persistence():
	
	def __init__(self):
		self.config = {
			'user': 'root',
			'password': 'p@ssword',
			'host': '127.0.0.1',
			'database': 'weather_app',
			'raise_on_warnings': True
		}

	def connect(self):
		try:
			self.cnx = mysql.connector.connect(**self.config) 
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your database's username or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
	 			print(err)
			raw_input()

	def login(self, username, pattern):
		self.connect()
		# This is unsafe
		query = "SELECT name,email,record_time FROM users WHERE users.name = '%s' AND users.pattern = '%s';" % (username,pattern)
		cursor = self.cnx.cursor()
		cursor.execute(query)
		# Comment the three previous lines and comment out the following to make it safe
		#query = "SELECT name,email,record_time FROM users WHERE users.name = '%s' AND users.pattern = '%s';"
		#cursor = self.cnx.cursor()
		#cursor.execute(query,(username,pattern))
		result = []
		for row in cursor:
			result.append(row)
		cursor.close()
		self.cnx.close()
		if len(result) > 0:
			user_logged = {
				'name': result[0][0],
				'mail': result[0][1],
				'wait': result[0][2]
			}
			return user_logged
		else:
			raise Exception("User not found")
