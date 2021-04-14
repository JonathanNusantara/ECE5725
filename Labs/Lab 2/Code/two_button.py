# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 2, 10-10-2020

import sys
import pygame
from pygame.locals import* # for event MOUSE variables
import os
import RPi.GPIO as GPIO
import time
import math

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
speed = [1, 1]
speed2 = [1, 2]

# Create screen
screen = pygame.display.set_mode(size)
screen.fill(BLACK)

# Create ball from image and create the rect
ball = pygame.image.load("magic_ball.png")
ball = pygame.transform.scale(ball, (60, 60)) # Scale the ball
ballrect = ball.get_rect(center = (100, 40)) # Set up center coordinates
ball2 = pygame.image.load("soccer_ball.png")
ball2= pygame.transform.scale(ball2, (60,60)) # Scale the ball
ball2rect = ball2.get_rect(center = (190, 170))

# Calculate ball radius and distance between midpoints
ball_rad = abs(ballrect.left - ballrect.right) / 2
ball2_rad = abs(ball2rect.left - ball2rect.right) / 2
min_distance = ball_rad + ball2_rad

# Prepare buttons
my_font = pygame.font.Font(None, 35)
my_buttons = {'start':(80,200), 'quit':(240,200)} # Make quit button

# Initialize clock to control frame speed
clock = pygame.time.Clock()

# Variable to store if program should continue looping
code_run = True

# Counter to allow ball to bounce before calculating
# distance between the two midpoints of ball
count = 0

# Display buttons
for my_text, text_pos in my_buttons.items():
	text_surface = my_font.render(my_text, True, WHITE)
	rect = text_surface.get_rect(center=text_pos)
	screen.blit(text_surface, rect)

msg = "" # Initialize msg to be printed
animate = False

while code_run and (time.time() - start_time) < 100:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()		
			GPIO.cleanup()
			sys.exit()
			
		if (event.type is MOUSEBUTTONDOWN):
			pos = pygame.mouse.get_pos()
		elif (event.type is MOUSEBUTTONUP):
			pos = pygame.mouse.get_pos()
			x,y = pos
			if y > 180 and x > 190:
				print("Quit button is pressed")
				code_run = False
			elif y > 180 and x < 120:
				print("start button")
				animate = True
			else:
				# If new press, update message	
				msg = "touch at " + str(x) + ", " + str(y)
	
	if animate == True:	
		# Calculate the ball position and distance between them	
		ball_center = [(ballrect.left + ballrect.right) / 2, (ballrect.top + ballrect.bottom) / 2]
		ball2_center = [(ball2rect.left + ball2rect.right) / 2, (ball2rect.top + ball2rect.bottom) / 2]
		distance = math.sqrt(math.pow(ball_center[0] - ball2_center[0], 2) + math.pow(ball_center[1] - ball2_center[1], 2))
	
		# Ball motion	
		ballrect = ballrect.move(speed)
		ball2rect = ball2rect.move(speed2)
	
		# Check if hit the wall
		if ballrect.left < 0 or ballrect.right > width:
			speed[0] = -speed[0]
		if ballrect.top < 0 or ballrect.bottom > height:
			speed[1] = -speed[1]
		if ball2rect.left < 0 or ball2rect.right > width:
			speed2[0] = -speed2[0]
		if ball2rect.top < 0 or ball2rect.bottom > height:
			speed2[1] = -speed2[1]
		
		# Check if the two balls collide
		# Counter is use to allow ball to move away from each other
		if distance <= min_distance and count > 10:
			speed[0] = -speed[0]
			speed[1] = -speed[1]
			speed2[0] = -speed2[0]
			speed2[1] = -speed2[1]
			count = 0 # reset counter
	
	# Clear workspace
	screen.fill(BLACK)
	
	# Display coordinates
	text_surface_msg = my_font.render(msg, True, WHITE)
	rect_msg = text_surface.get_rect(center= (100, 80))
	screen.blit(text_surface_msg, rect_msg)	
			
	
	
	if animate == True:	
		# Dislay ball animation
		screen.blit(ball, ballrect)
		screen.blit(ball2, ball2rect)
		
	# Re-display buttons
	for my_text, text_pos in my_buttons.items():
		text_surface = my_font.render(my_text, True, WHITE)
		rect = text_surface.get_rect(center=text_pos)
		screen.blit(text_surface, rect)
			
	pygame.display.flip()
				
	# If button 17 is pressed, then quit
	if GPIO.input(17) == 0:
		code_run = False	
					
	# Clock to set frame speed
	clock.tick(160)
	
	# Counter for ball collision
	count = count + 1
		
# Quit text file, pygame and clean GPIO
pygame.quit()		
GPIO.cleanup()
