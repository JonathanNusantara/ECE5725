# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 1, 09-27-2020

import RPi.GPIO as GPIO
import time
import subprocess

# Set numbering convention
GPIO.setmode(GPIO.BCM)

# Set GPIO channels for input
# Set the pins to be input and set initial value to be pull up resistor
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Monitor the button
while True:
	if GPIO.input(17) == 0: # Button to pause
		send_command = 'echo pause > video_fifo' # Set command string for mplayer command
		subprocess.check_output(send_command, shell = True) # Send command to terminal
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(22) == 0: # Button to fast-forward 10 sec
		send_command = 'echo seek 10 0 > video_fifo'
		subprocess.check_output(send_command, shell = True)
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(23) == 0: # Button to rewind 10 sec
		send_command = 'echo seek -10 0 > video_fifo'
		subprocess.check_output(send_command, shell = True)
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(27) == 0: # Button to quit mplayer
		send_command = 'echo quit > video_fifo'
		subprocess.check_output(send_command, shell = True)
		break # Quit the program
