# raspberryWeather
Course project for Security Analysis class at University of Ontario Institute of Technology. The main purpose of it was to get familiar with Raspberry Pi, Sense Hat and the security concepts learned during the semester.

The application records weather information periodically (temperature, humidity and pressure) using a Raspberry Pi add-on
board named Sense Hat (https://www.raspberrypi.org/products/sense-hat/) and send it to the user's email inbox. In order to
login, each user has to enter his username and an authentication pattern in the Sense Hat's LED Matrix. 

Users' information is stored in a local MySQL database.

We made the app with a SQL Injection vulnerability on purpose since it was condition asked in the assignement.If an user enter
in the Username's field the following string:

anything' OR 1=1 #

He will be granted access to the app as the first user stored in the Users' table.
