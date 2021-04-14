# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 3, 10-25-2020

import RPi.GPIO as GPIO
import time
import sys
import pygame
from pygame.locals import* # for event MOUSE variables
import os
import subprocess

# Run fix touchscreen script
subprocess.check_output("./fix_touchscreen", shell = True)

# Set start time to limit program run
start_time = time.time()

# Set numbering convention
GPIO.setmode(GPIO.BCM)

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1') # Display on PiTFT
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# Set GPIO channels
# Motor A
GPIO.setup(26, GPIO.OUT) #PWMA
GPIO.setup(5, GPIO.OUT) #AI1
GPIO.setup(6, GPIO.OUT) #AI2
# Motor B
GPIO.setup(20, GPIO.OUT) #PWMB
GPIO.setup(12, GPIO.OUT) #BI1
GPIO.setup(16, GPIO.OUT) #BI2

# PiTFT Buttons
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# External buttons 
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize pygame
pygame.init()

# Initialization
pygame.mouse.set_visible(False)
size = width, height = 320, 240
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0

# Create screen
screen = pygame.display.set_mode(size)
screen.fill(BLACK)

# Fonts and buttons
my_font = pygame.font.Font(None, 20)
my_buttons = {'STOP':(160, 120), 'RESUME':(160, 120), 'START':(100, 200),  'Left History':(60,20), 'Right History':(250,20), 'QUIT':(220,200)} # Make quit button

# Create queue from listfor motor control log
left_log = []
right_log = []

# Append logs with default content of Stop
for i in range(3):
	left_log.append(("Stop", 0))
	right_log.append(("Stop", 0))

# Setup coordinates for each log content
left_log_coordinate = [(60, 110), (60, 80), (60, 50)]
right_log_coordinate = [(250, 110), (250, 80), (250, 50)]

# Motor function
def control(motor_num, direction):
	if stop == False and start == True: # Only change motor mode if not in stop state and start button has been pressed
		if motor_num == 1: # left
			if direction == 0: # stop
				GPIO.output(5, 0) # Set AI1 to low
				GPIO.output(6, 0) # Set AI2 to low
				left_log.pop(0) # Remove first index
				left_log.append(("Stop", int(time.time() - start_time)))
			
			elif direction == 1: # cw
				GPIO.output(5, 1) # Set AI1 to high
				GPIO.output(6, 0) # Set AI2 to low
				left_log.pop(0)
				left_log.append(("Clkwise", int(time.time() - start_time)))
			
			elif direction == 2: # ccw
				GPIO.output(5, 0) # Set AI1 to low
				GPIO.output(6, 1) # Set AI2 to high
				left_log.pop(0)
				left_log.append(("Counter-Clk", int(time.time() - start_time)))
				
		elif motor_num == 2: # right
			if direction == 0: # stop
				GPIO.output(12, 0) # Set BI1 to low
				GPIO.output(16, 0) # Set BI2 to low
				right_log.pop(0)
				right_log.append(("Stop", int(time.time() - start_time)))
			
			elif direction == 1: # cw
				GPIO.output(12, 1) # Set BI1 to high
				GPIO.output(16, 0) # Set BI2 to low
				right_log.pop(0)
				right_log.append(("Clkwise", int(time.time() - start_time)))
			
			elif direction == 2: # ccw
				GPIO.output(12, 0) # Set BI1 to low
				GPIO.output(16, 1) # Set BI2 to high
				right_log.pop(0)
				right_log.append(("Counter-Clk", int(time.time() - start_time)))

freq = 50 # Initial frequency

p = GPIO.PWM(26, freq)
p2 = GPIO.PWM(20, freq)

GPIO.output(5, 0) # Set AI1 to low
GPIO.output(6, 0) # Set AI2 to low
GPIO.output(12, 0) # Set BI1 to low
GPIO.output(16, 0) # Set BI2 to low

# Define the callback function for each button
# Define the command to be passed to fifo for each button
def GPIO17_callback(channel):
	print("right motor, clockwise")
	control(2, 1)

def GPIO22_callback(channel):
	print("right motor, ccw")
	control(2, 2)

def GPIO23_callback(channel):
	print("left motor, clockwise")
	control(1, 1)

def GPIO27_callback(channel):
	print("left motor, ccw")
	control(1, 2)
	
def GPIO4_callback(channel):
	print("right motor, stop")
	control(2, 0)

def GPIO13_callback(channel):
	print("left motor, stop")
	control(1, 0)
	
# Event detection, set to falling, and bouncetime is set to prevent button bouncing error
GPIO.add_event_detect(17, GPIO.FALLING, callback = GPIO17_callback, bouncetime = 300)
GPIO.add_event_detect(22, GPIO.FALLING, callback = GPIO22_callback, bouncetime = 300)
GPIO.add_event_detect(23, GPIO.FALLING, callback = GPIO23_callback, bouncetime = 300)
GPIO.add_event_detect(27, GPIO.FALLING, callback = GPIO27_callback, bouncetime = 300)
GPIO.add_event_detect(4, GPIO.FALLING, callback = GPIO4_callback, bouncetime = 300)
GPIO.add_event_detect(13, GPIO.FALLING, callback = GPIO13_callback, bouncetime = 300)

# Variable to store if program should continue looping
code_run = True
stop = False
start = False
step = 1 # Initialize step at 1
required_time = 0
step_start_time = 0

p.start(75) # Start with dc = 25
p2.start(75)

while code_run: # Infinite while loop
    
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()		
			p.stop()
			p2.stop()
			GPIO.cleanup()
			sys.exit()
			
		if (event.type is MOUSEBUTTONDOWN):
			pos = pygame.mouse.get_pos()
		elif (event.type is MOUSEBUTTONUP):
			pos = pygame.mouse.get_pos()
			x,y = pos
			if y > 90 and y < 150 and x > 130 and x < 190:
				print("Stop button is pressed")
				if stop == False:
					# Stop both motors
					control(1, 0)
					control(2, 0)
					stop = True
				elif stop == True:
					print("Resume button is pressed")
					stop = False # Allow motor mode change
					
			elif y > 180 and y < 220 and x > 200 and x < 240:
				print("Quit button is pressed")
				code_run = False # Quit the while loop
				
			elif y > 180 and y < 220 and x > 80 and x < 120:
				print("Start button is pressed")
				start = True
	
	# Clear workspace
	screen.fill(BLACK)
	
	# Display history log
	for i in range(3): # Left
		dir_motor = left_log[i][0]
		time_motor = left_log[i][1]
		msg = dir_motor + "   " + str(time_motor) # message to be printed
		text_surface_log = my_font.render(msg, True, WHITE)
		rect_log = text_surface_log.get_rect(center= left_log_coordinate[i])
		screen.blit(text_surface_log, rect_log)	
	for i in range(3): # right
		dir_motor = right_log[i][0]
		time_motor = right_log[i][1]
		msg = dir_motor + "   " + str(time_motor) # message to be printed
		text_surface_log = my_font.render(msg, True, WHITE)
		rect_log = text_surface_log.get_rect(center= right_log_coordinate[i])
		screen.blit(text_surface_log, rect_log)		
		
	# Display buttons
	for my_text, text_pos in my_buttons.items():
		if my_text == "STOP":
			if stop == False:
				pygame.draw.circle(screen, RED, text_pos, 40)
				text_surface = my_font.render(my_text, True, WHITE)
				rect = text_surface.get_rect(center=text_pos)
				screen.blit(text_surface, rect)
		elif my_text == "RESUME":
			if stop == True:
				pygame.draw.circle(screen, GREEN, text_pos, 40)
				text_surface = my_font.render(my_text, True, BLACK)
				rect = text_surface.get_rect(center=text_pos)
				screen.blit(text_surface, rect)
		else :		
			text_surface = my_font.render(my_text, True, WHITE)
			rect = text_surface.get_rect(center=text_pos)
			screen.blit(text_surface, rect)
			
	pygame.display.flip()
	
	if start == True and stop == False:
		if step == 1 and (time.time() - step_start_time) > required_time: # Forward
			control(1, 2)
			control(2, 1)
			required_time = 1
			step_start_time = time.time()
			step = 2
		
		elif step == 2 and (time.time() - step_start_time) > required_time: # Stop
			control(1, 0)
			control(2, 0)
			required_time = 1
			step_start_time = time.time()
			step = 3
			
		elif step == 3 and (time.time() - step_start_time) > required_time: # Backward
			control(1, 1)
			control(2, 2)
			required_time = 1
			step_start_time = time.time()
			step = 4
			
		elif step == 4 and (time.time() - step_start_time) > required_time: # Left
			control(1, 1)
			control(2, 1)
			required_time = 1
			step_start_time = time.time()
			step = 5	
			
		elif step == 5 and (time.time() - step_start_time) > required_time: # Stop
			control(1, 0)
			control(2, 0)
			required_time = 1
			step_start_time = time.time()
			step = 6
			
		elif step == 6 and (time.time() - step_start_time) > required_time: # Right
			control(1, 2)
			control(2, 2)
			required_time = 1
			step_start_time = time.time()
			step = 7
			
		elif step == 7 and (time.time() - step_start_time) > required_time: # Stop
			control(1, 0)
			control(2, 0)
			required_time = 1
			step_start_time = time.time()
			step = 1
	
	if (time.time() - start_time) > 30: # Timeout
		code_run = False
	
		
p.stop()
p2.stop()
GPIO.cleanup()
