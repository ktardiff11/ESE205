import RPi.GPIO as GPIO
import time
from mod4_funcs import ultrasonic_init as u_init
from mod4_funcs import ultrasonic_read 

TRIG = 15  # define input and output pins
ECHO = 16

u_init(TRIG, ECHO)

time_start = time.time()    
distance = ultrasonic_read(TRIG, ECHO)
time_end = time.time()

print (f'Distance Away: {distance:.2f} cm')
print (f'Taken in {time_end-time_start:.3f} seconds')

GPIO.cleanup()              # reset the GPIO 
