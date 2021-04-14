# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 3, 10-25-2020

import RPi.GPIO as GPIO
import time

# Set start time to limit program run
start_time = time.time()

# Set numbering convention
GPIO.setmode(GPIO.BCM)

# Setup GPIO pin as output
GPIO.setup(26, GPIO.OUT) #PWMA

# Set variable as PWM
p = GPIO.PWM(26, 1) # Freq is 1Hz

p.start(50) # Set duty cycle to 50%

while (time.time()-start_time) < 10: # Set a timeout
	user = input("Input a frequency: ")
	p.ChangeFrequency(user) # Change frequency based on user input

p.stop()
GPIO.cleanup()
