# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 2, 10-10-2020

import sys
import pygame
import os
import RPi.GPIO as GPIO
import time
import math

# Set up GPIO and display settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1') # Display on PiTFT

# Set start time to limit program run
start_time = time.time()

# Initialize pygame
pygame.init()

# Initialization
pygame.mouse.set_visible(False)
size = width, height = 320, 240
speed = [1, 1]
speed2 = [1, 2]
black = 0, 0, 0

# Create screen size
screen = pygame.display.set_mode(size)

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

# Initialize clock to control frame speed
clock = pygame.time.Clock()

# Variable to store if program should continue looping
code_run = True

# Counter to allow ball to bounce before calculating
# distance between the two midpoints of ball
count = 0

# While loop to allow ball animation
while code_run and (time.time() - start_time) < 10:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
	
	# Calculate the ball position and distance between them	
	ball_center = [(ballrect.left + ballrect.right) / 2, (ballrect.top + ballrect.bottom) / 2]
	ball2_center = [(ball2rect.left + ball2rect.right) / 2, (ball2rect.top + ball2rect.bottom) / 2]
	distance = math.sqrt(math.pow(ball_center[0] - ball2_center[0], 2) + math.pow(ball_center[1] - ball2_center[1], 2))
	
	# Ball motion	
	ballrect = ballrect.move(speed)
	ball2rect = ball2rect.move(speed2)
	
	# Check if hit the wall
	# In the case of a ball colliding with a ball
	# and a wall at the same time
	# wait for some time (counter val) to allow ball to move
	if count > 3:  
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
	
	# Dislay animation in workspace and display	
	screen.fill(black)
	screen.blit(ball, ballrect)
	screen.blit(ball2, ball2rect)
	pygame.display.flip()
	
	# If button 17 is pressed, then quit
	if GPIO.input(17) == 0:
		code_run = False
	
	# Clock to set frame speed
	clock.tick(200)
	
	# Counter for ball collision
	count = count + 1
		
# Quit pygame and clean GPIO		
pygame.quit()		
GPIO.cleanup()
		
