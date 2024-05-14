import smbus		
import time
import argparse       
from mod4_funcs import MPU_Read
from mod4_funcs import MPU_Init 
from mod4_funcs import movingAvg
    
bus = smbus.SMBus(1) 	        

MPU_Init(bus)

DEBUG = False
parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--tim', type=int, default=5)
parser.add_argument('--delay', type=int, default=0.1)
parser.add_argument('--out', type=int, default=1)
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()

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

t = [0]*MAXSIZE

DEBUG = args.debug
    
time_start = time.time()
cur_time = time_start
i = 0
counter = 0

print (" Reading Data of Gyroscope and Accelerometer")


while time_start + args.tim > cur_time:
  cur_time = time.time(); 

  if time_start + counter * args.delay < cur_time:
    i = counter%MAXSIZE 
    Ax[i] = MPU_Read(bus, 1)
    Ay[i] = MPU_Read(bus, 2)
    Az[i] = MPU_Read(bus, 3)

    Gx[i] = MPU_Read(bus, 4)
    Gy[i] = MPU_Read(bus, 5)
    Gz[i] = MPU_Read(bus, 6)

    AxMA[i] = movingAvg(Ax, counter)
    AyMA[i] = movingAvg(Ay, counter)
    AzMA[i] = movingAvg(Az, counter)

    GxMA[i] = movingAvg(Gx, counter)
    GyMA[i] = movingAvg(Gy, counter)
    GzMA[i] = movingAvg(Gz, counter)

    counter = counter + 1
    t[i] = cur_time - time_start
    
    if DEBUG:
      print (f'Gx: {Gx[i]:0.2f} /s\tGy: {Gy[i]:0.2f} /s\tGz: {Gz[i]:0.2f} /s\t')
      print (f'Ax: {Ax[i]:0.2f} g\tAy: {Ay[i]:0.2f} g\tAz: {Az[i]:0.2f} g')

  time.sleep(0.001)

datafile = open("data.txt", "w")

# Function
def data (out, position, time):
  if out == 1:
    datafile.write(f'{Ax[position]:0.2f}\t{AxMA[position]:0.2f}\t{time}\n')
  if out == 2:
    datafile.write(f'{Ay[position]:0.2f}\t{AyMA[position]:0.2f}\t{time}\n')
  if out == 3:
    datafile.write(f'{Az[position]:0.2f}\t{AzMA[position]:0.2f}\t{time}\n')
  if out == 4:
    datafile.write(f'{Gx[position]:0.2f}\t{GxMA[position]:0.2f}\t{time}\n')
  if out == 5:
    datafile.write(f'{Gy[position]:0.2f}\t{GyMA[position]:0.2f}\t{time}\n')
  if out == 6:
    datafile.write(f'{Gz[position]:0.2f}\t{GzMA[position]:0.2f}\t{time}\n')

for i in range(counter):
  data(args.out, i, t[i])

datafile.close()
