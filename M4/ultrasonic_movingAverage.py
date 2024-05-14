import RPi.GPIO as GPIO
import time
from mod4_funcs import ultrasonic_init as u_init
from mod4_funcs import ultrasonic_read
from mod4_funcs import movingAvg

TRIG = 15   # define input and output pins
ECHO = 16

u_init(TRIG, ECHO)

start_time = time.time()
cur_time   = start_time
mesg_time  = start_time
counter    = 0
debug      = True

MAXSIZE    = 1000           # create some arrays with 0's
times      = [0]*MAXSIZE
distances  = [0]*MAXSIZE
MA_dist    = [0]*MAXSIZE

delay      = 0.2            # delay between samples
loop_time  = 10             # time to run loop

while (start_time + loop_time > cur_time):
   cur_time = time.time()
   if (start_time + counter*delay < cur_time):
      i = counter%MAXSIZE
      distances[i] = ultrasonic_read(TRIG, ECHO)
      # MA with window of 3 (default) and wrap (default)
      MA_dist[i] = movingAvg(distances, counter)
      times[i]   = cur_time - start_time
      if debug: print(f'{times[i]:0.2f}\t{distances[i]}\t{MA_dist[i]}')
      counter = counter + 1
   time.sleep(0.001)         # some short delay to avoid busy waits

datafile = open("distance.txt", "w")
for i in range(counter):
   datafile.write(f'{times[i]:0.2f}\t{distances[i]}\t{MA_dist[i]}\n')
datafile.close()

GPIO.cleanup()              # reset the GPIO
