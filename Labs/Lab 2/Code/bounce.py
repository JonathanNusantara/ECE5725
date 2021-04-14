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
speed = [1,1]
black = 0, 0, 0

# Create screen size
screen = pygame.display.set_mode(size)

# Create ball from image and create the rect
ball = pygame.image.load("magic_ball.png")
ballrect = ball.get_rect()

code_run = True

# While loop to allow ball animation
while code_run and (time.time() - start_time) < 10: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
	
	# Change ball position	
	ballrect = ballrect.move(speed)
	
	# Check if hit the wall
	if ballrect.left < 0 or ballrect.right > width:
		speed[0] = -speed[0]
	if ballrect.top < 0 or ballrect.bottom > height:
		speed[1] = -speed[1]
	
	# Display ball in workspace and screen	
	screen.fill(black)
	screen.blit(ball, ballrect)
	pygame.display.flip()
	
	# Quit if buttin 17 is pressed
	if GPIO.input(17) == 0:
		code_run = False
		
pygame.quit()		
GPIO.cleanup()
