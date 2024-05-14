import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
import sys
from time import sleep     # Import the sleep from time module
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering


ITER_COUNT = 5            # Depends on the input.
pin1 = 3

if(len(sys.argv) >1) : ITER_COUNT = int(sys.argv[1])
GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)   
n =  int

while ITER_COUNT > 0: # Run ITER_COUNT times
   ITER_COUNT -= 1 # Decrement counter
   GPIO.output(pin1, GPIO.HIGH) # Turn on
   sleep(1)                     # Sleep for 1 second
   GPIO.output(pin1, GPIO.LOW)  # Turn off
   sleep(1)                     # Sleep for 1 second
GPIO.cleanup()
