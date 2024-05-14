import smbus			#import SMBus module of I2C
from time import sleep          #import
from mod4_funcs import MPU_Read
from mod4_funcs import MPU_Init 

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards

MPU_Init(bus)

print (" Reading Data of Gyroscope and Accelerometer")

while True:
	
   Ax = MPU_Read(bus, 1)
   Ay = MPU_Read(bus, 2)
   Az = MPU_Read(bus, 3)

   Gx = MPU_Read(bus, 4)
   Gy = MPU_Read(bus, 5)
   Gz = MPU_Read(bus, 6)
	
   print (f'Gx: {Gx:0.2f} \u00b0/s\tGy: {Gy:0.2f} \u00b0/s\tGz: {Gz:0.2f} \u00b0/s\t', end=' ')
   print (f'Ax: {Ax:0.2f} g\tAy: {Ay:0.2f} g\tAz: {Az:0.2f} g')
   sleep(0.1)

