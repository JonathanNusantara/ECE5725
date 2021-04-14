# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 2, 10-10-2020

import sys
import pygame
import os
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0') # Display on monitor

start_time = time.time()

# Initialize pygame
pygame.init()

# Initialization
size = width, height = 320, 240
speed = [2, 2]
speed2 = [1, 1]
black = 0, 0, 0

# Create screen size
screen = pygame.display.set_mode(size)

# Create ball from image and create the rect
ball = pygame.image.load("magic_ball.png")
ballrect = ball.get_rect()
ball2 = pygame.image.load("soccer_ball.png")
ball2rect = ball2.get_rect()

code_run = True

# While loop to allow ball animation
while code_run and (time.time() - start_time) < 10:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		
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
		
	# Dislay animation in workspace and display			
	screen.fill(black)
	screen.blit(ball, ballrect)
	screen.blit(ball2, ball2rect)
	pygame.display.flip()
	
	# If GPIO 17 is pressed, quit
	if GPIO.input(17) == 0:
		code_run = False
		
# Quit pygame and clean GPIO		
pygame.quit()		
GPIO.cleanup()
		
