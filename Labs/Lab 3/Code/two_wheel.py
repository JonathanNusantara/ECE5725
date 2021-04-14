# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 3, 10-25-2020

import RPi.GPIO as GPIO
import time

# Set start time to limit program run
start_time = time.time()

# Set numbering convention
GPIO.setmode(GPIO.BCM)

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


def control(motor_num, direction):
	if motor_num == 1: # left
		if direction == 0: # stop
			GPIO.output(5, 0) # Set AI1 to low
			GPIO.output(6, 0) # Set AI2 to low
			
		elif direction == 1: # cw
			GPIO.output(5, 1) # Set AI1 to high
			GPIO.output(6, 0) # Set AI2 to low
			
		elif direction == 2: # ccw
			GPIO.output(5, 0) # Set AI1 to low
			GPIO.output(6, 1) # Set AI2 to high
				
	elif motor_num == 2: # right
		if direction == 0: # stop
			GPIO.output(12, 0) # Set BI1 to low
			GPIO.output(16, 0) # Set BI2 to low
			
		elif direction == 1: # cw
			GPIO.output(12, 1) # Set BI1 to high
			GPIO.output(16, 0) # Set BI2 to low
			
		elif direction == 2: # ccw
			GPIO.output(12, 0) # Set BI1 to low
			GPIO.output(16, 1) # Set BI2 to high

freq = 50 # Initial frequency

p = GPIO.PWM(26, freq)
p2 = GPIO.PWM(20, freq)

GPIO.output(5, 0) # Set AI1 to low
GPIO.output(6, 0) # Set AI2 to low
GPIO.output(12, 0) # Set BI1 to low
GPIO.output(16, 0) # Set BI2 to low

p.start(100) # Start with dc = 100
p2.start(100)

code_run = True
while code_run: # Infinite while loop
	if GPIO.input(17) == 0: # Check if GPIO is low
		print("right motor, clockwise")
		control(2, 1)
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(22) == 0: # Check if GPIO is low
		print("right motor, ccw")
		control(2, 2)
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(23) == 0: # Check if GPIO is low
		print("left motor, clockwise")
		control(1, 1)
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(27) == 0: # Check if GPIO is low
		print("left motor, ccw")
		control(1, 2)
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(4) == 0: # Check if GPIO is low
		print("right motor, stop")
		control(2, 0)
		time.sleep(.3) # Prevent button bouncing
	elif GPIO.input(13) == 0: # Check if GPIO is low
		print("left motor, stop")
		control(1, 0)
		time.sleep(.3) # Prevent button bouncing
	if (time.time() - start_time) > 10:
		code_run = False	

p.stop()
p2.stop()
GPIO.cleanup()
