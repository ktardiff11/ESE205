import smbus		
import time        
from mod4_funcs import MPU_Read
from mod4_funcs import MPU_Init 
import argparse
    
bus = smbus.SMBus(1) 	        

MPU_Init(bus)

DEBUG = False
parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--tim', type=int, default=5)
parser.add_argument('--delay', type=int, default=0.1)
parser.add_argument('--out', type=int, default=1)
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()

DEBUG = args.debug

# Function
def data (out):
  if out == 1:
      print (f'Ax: {Ax:0.2f} g\t')
  elif out == 2:
    print (f'Ay: {Ay:0.2f} g\t')
  elif out == 3:
    print (f'Az: {Az:0.2f} g\t')
  elif out == 4:
    print (f'Gx: {Gx:0.2f} g\t')
  elif out == 5:
    print (f'Gy: {Gy:0.2f} g\t')
  elif args.out == 6:
    print (f'Gz: {Gz:0.2f} g\t')
    
time_start = time.time()
cur_time = time_start
i = 0

print (" Reading Data of Gyroscope and Accelerometer")


while time_start + args.tim > cur_time:
  cur_time = time.time(); 

  if time_start + i * args.delay < cur_time:
  
    Ax = MPU_Read(bus, 1)
    Ay = MPU_Read(bus, 2)
    Az = MPU_Read(bus, 3)

    Gx = MPU_Read(bus, 4)
    Gy = MPU_Read(bus, 5)
    Gz = MPU_Read(bus, 6)

    data(args.out)

    if DEBUG:
      print (f'Gx: {Gx:0.2f} \u00b0/s\tGy: {Gy:0.2f} \u00b0/s\tGz: {Gz:0.2f} \u00b0/s\t', end=' ')
      print (f'Ax: {Ax:0.2f} g\tAy: {Ay:0.2f} g\tAz: {Az:0.2f} g')

  time.sleep(0.001)
