# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 1, 09-27-2020

import RPi.GPIO as GPIO
import time

# Set numbering convention
GPIO.setmode(GPIO.BCM)

# Set GPIO channels for input
# Set pin 17 to be input and set initial value to be pulled up resistor
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Monitor the button
while True:
	if GPIO.input(17) == 0: # If low
		print("Button 17 has been pressed")
		time.sleep(.3) # Prevent button bouncing
