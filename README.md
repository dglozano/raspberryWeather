# raspberryWeather
This a simple course project we made to get familiar with the Raspberry Pi and Sense Hat.

We have a MYSQL database locally with one table named "users" that stores the username, email, waiting
between recordings of the weather and the authentication pattern for each user.

In order to log in, you need to provide the username and then introduce the authentication pattern in 
the Sense Hat LED matrix using the joystick. Once logged in, the Sense Hat record the weather conditions
every X seconds specified by the logged user and send them to his email.

We made the app with a SQL Injection vulnerability in porpose. If you enter in the Username field
the following: " anything' OR 1=1 # " you will be granted access to the app as the firs user stored 
in the table.
