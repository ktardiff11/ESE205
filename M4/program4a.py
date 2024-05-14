import RPi.GPIO as GPIO
import time
import argparse
from mod4_funcs import ultrasonic_init as u_init
from mod4_funcs import ultrasonic_read
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

TRIG = 15  # define input and output pins
ECHO = 16

# set up the input and output pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, False)
GPIO.setup(ECHO, GPIO.IN)

parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--tim', type=int, default=5)
parser.add_argument('--delay', type=int, default=0.1)
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()
DEBUG = False
DEBUG = args.debug

u_init(TRIG, ECHO)

time_start = time.time()
cur_time = time_start
i = 0

while time_start + args.tim > cur_time:
  cur_time = time.time(); 

  if time_start + i * args.delay < cur_time:
    start = time.time()
    distance = ultrasonic_read(TRIG, ECHO)
    end = time.time()

    # Speed of sound 34300 cm/sec
    total_distance = (end - start) * 34300

    # Divide by 2, account for return trip for signal
    print (f'Distance Away: {distance/2:.2f} cm')
    print (f'Taken in {end-start:.3f} seconds')
    if DEBUG:
      print(f'{time.time() - time_start}')

  time.sleep(0.001)


GPIO.cleanup
