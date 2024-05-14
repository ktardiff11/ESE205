import RPi.GPIO as GPIO
import time
import argparse
import smbus
from mod4_funcs import ultrasonic_init as u_init
from mod4_funcs import ultrasonic_read
from mod4_funcs import MPU_Read
from mod4_funcs import MPU_Init 
from mod4_funcs import movingAvg
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

bus = smbus.SMBus(1)

MPU_Init(bus)

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

MAXSIZE = 1000
Ax = [0]*MAXSIZE
AxMA = [0]*MAXSIZE
Ay = [0]*MAXSIZE
AyMA = [0]*MAXSIZE
Az = [0]*MAXSIZE
AzMA = [0]*MAXSIZE

Gx = [0]*MAXSIZE
GxMA = [0]*MAXSIZE
Gy = [0]*MAXSIZE
GyMA = [0]*MAXSIZE
Gz = [0]*MAXSIZE
GzMA = [0]*MAXSIZE

distances = [0]*MAXSIZE
MovAvgdist = [0]*MAXSIZE 
t = [0]*MAXSIZE

u_init(TRIG, ECHO)

time_start = time.time()
cur_time = time_start
i = 0
counter = 0

while time_start + args.tim > cur_time:
  cur_time = time.time(); 

  if time_start + i * args.delay < cur_time:
    i = counter%MAXSIZE
    t[i] = time.time() - time_start
  
    Ax[i] = MPU_Read(bus, 1)
    Ay[i] = MPU_Read(bus, 2)
    Az[i] = MPU_Read(bus, 3)

    Gx[i] = MPU_Read(bus, 4)
    Gy[i] = MPU_Read(bus, 5)
    Gz[i] = MPU_Read(bus, 6)


    
    distances[i] = ultrasonic_read(TRIG, ECHO)

    t[i] = cur_time - time_start


    if DEBUG:
      print(f'{t[i]}')

    counter = counter + 1

  time.sleep(0.001)


datafile = open("dataWalk.txt", "w")


for i in range(counter):
  datafile.write(f'{distances[i]:0.2f}\t{Ax[i]:0.2f}\t{Ay[i]:0.2f}\t{Az[i]:0.2f}\t{Gx[i]:0.2f}\t{Gy[i]:0.2f}\t{Gz[i]:0.2f}\t{t[i]}\n')

datafile.close()

GPIO.cleanup
