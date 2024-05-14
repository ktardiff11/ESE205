import RPi.GPIO as GPIO
import time
import sys
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Setting variables
INPUT_PIN = 5
LED_PIN = 11

State = False
ITER_COUNT = 20


# Setting up pins
GPIO.setup(INPUT_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)


for i in range(0, ITER_COUNT): 

	if State:
		if not(GPIO.input(INPUT_PIN)):
			State = not(State)
			GPIO.output(LED_PIN, False)
			
	elif not(State):
		if GPIO.input(INPUT_PIN):				
			State = not(State)
			GPIO.output(LED_PIN, True)

	time.sleep(1)
GPIO.cleanup()
