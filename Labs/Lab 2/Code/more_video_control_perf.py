# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 2, 10-10-2020

import RPi.GPIO as GPIO
import time
import subprocess

start_time = time.time()

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
while code_run and (time.time() - start_time) < 10: # Infinite while loop
	#time.sleep(0.00002)
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
		code_run = False # Quit the program
	elif GPIO.input(19) == 0: # Button to fast-forward 30 sec
		send_command = 'echo seek 30 0 > video_fifo'
		subprocess.check_output(send_command, shell = True)
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(26) == 0: # Button to rewind 30 sec
		send_command = 'echo seek -30 0 > video_fifo'
		subprocess.check_output(send_command, shell = True)
		time.sleep(.3) # Prevent button bouncing		
