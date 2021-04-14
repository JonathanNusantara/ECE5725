# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 2, 10-10-2020

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

# Set up external buttons for Lab 2
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define the callback function for each button
# Define the command to be passed to fifo for each button
def GPIO17_callback(channel):
	send_command = 'echo pause > video_fifo'
	subprocess.check_output(send_command, shell = True)

def GPIO19_callback(channel):
	send_command = 'echo seek 30 0 > video_fifo'
	subprocess.check_output(send_command, shell = True)

def GPIO22_callback(channel):
	send_command = 'echo seek 10 0 > video_fifo'
	subprocess.check_output(send_command, shell = True)

def GPIO23_callback(channel):
	send_command = 'echo seek -10 0 > video_fifo'
	subprocess.check_output(send_command, shell = True)

def GPIO26_callback(channel):
	send_command = 'echo seek -30 0 > video_fifo'
	subprocess.check_output(send_command, shell = True)

#def GPIO27_callback(channel):
	#send_command = 'echo quit > video_fifo'
	#subprocess.check_output(send_command, shell = True)


# Event detection, set to falling, and bouncetime is set to prevent button bouncing error
GPIO.add_event_detect(17, GPIO.FALLING, callback = GPIO17_callback, bouncetime = 300)
GPIO.add_event_detect(19, GPIO.FALLING, callback = GPIO19_callback, bouncetime = 300)
GPIO.add_event_detect(22, GPIO.FALLING, callback = GPIO22_callback, bouncetime = 300)
GPIO.add_event_detect(23, GPIO.FALLING, callback = GPIO23_callback, bouncetime = 300)
GPIO.add_event_detect(26, GPIO.FALLING, callback = GPIO26_callback, bouncetime = 300)

try: # Wait for button 27 to be pressed
	GPIO.wait_for_edge(27, GPIO.FALLING, timeout = 10000)
	#send_command = 'echo quit > video_fifo'
	#subprocess.check_output(send_command, shell = True)
	
except KeyboardInterrupt:
	GPIO.cleanup() # GPIO clean when ctrl + c is passed
	
GPIO.cleanup()
