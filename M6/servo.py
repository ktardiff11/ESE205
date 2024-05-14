import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

# Define pin, frequency and duty cycle
PWM_pin   = 3 
freq      = 50
dutyCycle = 4 

# Configure pin for output
GPIO.setup(PWM_pin, GPIO.OUT)

# Create PWM instance for pin w freqency
pwm = GPIO.PWM(PWM_pin, freq) 
# Start the PWM object
pwm.start(dutyCycle)
time.sleep(1)           # let it sit for a second

# Change the duty cycle
dutyCycle = 8
pwm.ChangeDutyCycle(dutyCycle)
time.sleep(0.1)         # give it time to move 

# Stop the output for the PWM pin 
pwm.stop()
GPIO.cleanup()
