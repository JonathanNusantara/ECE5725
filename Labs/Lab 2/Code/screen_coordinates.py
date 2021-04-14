# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 2, 10-10-2020

import sys
import pygame
from pygame.locals import* # for event MOUSE variables
import os
import RPi.GPIO as GPIO
import time

# Store initial start time
start_time = time.time()

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1') # Display on PiTFT
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# Initialize pygame
pygame.init()

# Initialization
pygame.mouse.set_visible(False)
size = width, height = 320, 240
WHITE = 255, 255, 255
BLACK = 0, 0, 0

# Create screen
screen = pygame.display.set_mode(size)
screen.fill(BLACK)

# Prepare buttons
my_font = pygame.font.Font(None, 35)
my_buttons = {'quit':(240,180)} # Make quit button

# Initialize clock to control frame speed
clock = pygame.time.Clock()

# Variable to store if program should continue looping
code_run = True

x = 0
y = 0

# Display buttons
for my_text, text_pos in my_buttons.items():
	text_surface = my_font.render(my_text, True, WHITE)
	rect = text_surface.get_rect(center=text_pos)
	screen.blit(text_surface, rect)

# Open txt file to store coordinates
text_file = open("touch_coordinates.txt", "w")
while code_run and (time.time() - start_time) < 20:
	

	# Check touchscreen
	for event in pygame.event.get():
		if (event.type is MOUSEBUTTONDOWN):
			pos = pygame.mouse.get_pos()
		elif (event.type is MOUSEBUTTONUP):
			pos = pygame.mouse.get_pos()
			x,y = pos
			if y > 160 and x > 190:
				print("Quit button is pressed")
				code_run = False
				
			# Re-display buttons and message every touch	
			screen.fill(BLACK)
			
			# Re-display buttons
			for my_text, text_pos in my_buttons.items():
				text_surface = my_font.render(my_text, True, WHITE)
				rect = text_surface.get_rect(center=text_pos)
				screen.blit(text_surface, rect)
				
			msg = "touch at " + str(x) + ", " + str(y)
			print(msg)
			text_file.write(msg + "\n")
			text_surface_msg = my_font.render(msg, True, WHITE)
			rect_msg = text_surface.get_rect(center= (100, 80))
			screen.blit(text_surface_msg, rect_msg)	

	pygame.display.flip()
				
	# If button 17 is pressed, then quit
	if GPIO.input(17) == 0:
		code_run = False	
					
	# Clock to set frame speed
	clock.tick(20)				
# Quit text file, pygame and clean GPIO
text_file.close()
pygame.quit()		
GPIO.cleanup()
