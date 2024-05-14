import RPi.GPIO as GPIO
import time
import argparse
GPIO.setmode(GPIO.BOARD)

# Define pin, frequency and duty cycle
PWM_pin = 3
freq = 50
dutyCycle = 4 # Values 0 - 100 (represents 4%, ~27 deg)

# Configure pin for output
GPIO.setup(PWM_pin, GPIO.OUT)

parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--low', type=float, default=3)
parser.add_argument('--upp', type=float, default=14)
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()
DEBUG = False
DEBUG = args.debug

# Create PWM instance for pin w freqency
pwm = GPIO.PWM(PWM_pin, freq)

# Start the PWM object
pwm.start(dutyCycle)
time.sleep(1) # let it sit for a second

while True:
    # Get user input for new duty cycle
    newDutyCycle = int(input(f'Enter duty cycle between {args.low}% and {args.upp}% (0 to exit): '))
        
    if DEBUG:
        print(f'New Duty Cycle: {newDutyCycle}')

    if newDutyCycle == 0:
        break 
        
    if args.low <= newDutyCycle <= args.upp:
        pwm.ChangeDutyCycle(newDutyCycle)
        time.sleep(1) 
    else:
        print(f'Invalid duty cycle!')

# Stop the output for the PWM pin
pwm.stop()
GPIO.cleanup()
