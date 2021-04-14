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


freq = 50 # Initial frequency
dc = 0 # Initial dc

dc_list = [0, 25, 50, 100]

p = GPIO.PWM(26, freq)

GPIO.output(5, 0) # Set AI1 to low
GPIO.output(6, 0) # Set AI2 to low

p.start(dc) # Start with dc = 0

GPIO.output(5, 1) # Set AI1 to high
for i in dc_list:
	print("dc = " + str(i))
	p.ChangeDutyCycle(i)
	time.sleep(3)

GPIO.output(5, 0) # Set AI1 to low
GPIO.output(6, 1) # Set AI2 to high
for i in dc_list:
	print("dc = " + str(i))
	p.ChangeDutyCycle(i)
	time.sleep(3)

p.ChangeDutyCycle(0)

p.stop()
GPIO.cleanup()
