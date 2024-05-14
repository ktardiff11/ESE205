import RPi.GPIO as GPIO
import time
import sys
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

blink = int(input('Pick a number for blink rate (s):'))
totalTime = int(input('Pick a number for program length (s):'))
ITER_COUNT = int(totalTime/blink)


# Setting variables
INPUT_PIN = 5
LED_PIN = 11

off = 'OFF'
on = 'ON'

LED_IS_ON = False

# Setting up pins
GPIO.setup(INPUT_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
start = time.time()
with open('data.txt', 'w') as data:
	for i in range(0, ITER_COUNT):

		if GPIO.input(INPUT_PIN):
			GPIO.output(LED_PIN, LED_IS_ON)
			data.write(f'{time.time()-start:1.0f}\t{on}\n')
			LED_IS_ON = not(LED_IS_ON)
			time.sleep(blink)

		else:
			data.write(f'{time.time()-start:1.0f}\t{off}\n')
			GPIO.output(LED_PIN, False)
			time.sleep(blink)
GPIO.cleanup()
