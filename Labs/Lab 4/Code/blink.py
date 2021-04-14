# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 4, 11-08-2020

import RPi.GPIO as GPIO
import time

# Set start time to limit program run
start_time = time.time()

# Set numbering convention
GPIO.setmode(GPIO.BCM)

# Setup GPIO pin as output
GPIO.setup(26, GPIO.OUT) #PWMA

# Set variable as PWM
freq = 100
p = GPIO.PWM(26, freq) # Freq is 1Hz

p.start(50) # Set duty cycle to 50%

current_time = 1

while (time.time()-start_time) < 60: # Set a timeout
	if (time.time() - current_time) > 1: # change freq every second
		freq = freq + 100
		p.ChangeFrequency(freq) # Change frequency based on user input
		current_time = time.time()

p.stop()
GPIO.cleanup()
