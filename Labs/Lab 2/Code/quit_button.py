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
my_font = pygame.font.Font(None, 50)
my_buttons = {'quit':(240,180)} # Make quit button

# Display buttons
for my_text, text_pos in my_buttons.items():
	text_surface = my_font.render(my_text, True, WHITE)
	rect = text_surface.get_rect(center=text_pos)
	screen.blit(text_surface, rect)
pygame.display.flip()

# Variable to store if program should continue looping
code_run = True

while code_run and (time.time() - start_time) < 10:
	# Check touchscreen
	for event in pygame.event.get():
		if (event.type is MOUSEBUTTONDOWN):
			pos = pygame.mouse.get_pos()
		elif (event.type is MOUSEBUTTONUP):
			pos = pygame.mouse.get_pos()
			x,y = pos
			if y > 120:
				if x > 160:
					print("Quit button is pressed")
					code_run = False
					
	# If button 17 is pressed, then quit
	if GPIO.input(17) == 0:
		code_run = False				
					
# Quit pygame and clean GPIO		
pygame.quit()		
GPIO.cleanup()
