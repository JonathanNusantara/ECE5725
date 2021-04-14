# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 2, 10-10-2020

import RPi.GPIO as GPIO
import time

# Set numbering convention
GPIO.setmode(GPIO.BCM)

# Set GPIO channels for input
# Set the pins to be input and set initial value to be pull up resistor
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up external buttons for Lab 2
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Monitor the button
code_run = True
while code_run: # Infinite while loop
	if GPIO.input(17) == 0: # Check if GPIO is low
		print("Button 17 has been pressed")
		time.sleep(.3) # Prevent button bouncing
		code_run = False # Quit from the python program
	elif GPIO.input(22) == 0: # Check if GPIO is low
		print("Button 22 has been pressed")	
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(23) == 0: # Check if GPIO is low
		print("Button 23 has been pressed")		
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(27) == 0: # Check if GPIO is low
		print("Button 27 has been pressed")		
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(19) == 0: # Check if GPIO is low
		print("Button 19 has been pressed")		
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(26) == 0: # Check if GPIO is low
		print("Button 26 has been pressed")		
		time.sleep(.3) # Prevent button bouncing		
