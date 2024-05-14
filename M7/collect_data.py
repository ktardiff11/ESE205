import RPi.GPIO as GPIO
import argparse
import time
import numpy as np
import matplotlib
matplotlib.use('Pdf')
import matplotlib.pyplot as plt
import Adafruit_MCP3008
from Adafruit_GPIO.GPIO import RPiGPIOAdapter as Adafruit_GPIO_Adapter
import mod7_func as motor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)



ADC_pin = 0

# Defining motor pins
in1 = 16
in2 = 18
en  = 22


parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--tim', type=float, default=5)
parser.add_argument('--delay', type=float, default=0.01)
parser.add_argument('--duty', type=float, default=50.0)
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()
DEBUG = False
DEBUG = args.debug

# Init Motor
pwm_pin   = motor.motor_init(in1, in2, en, 200, args.duty)

motor.motor_direction(in1, in2, 1)
time.sleep(5)

# SPI configuration
CLK  = 23
MISO = 21
MOSI = 19
CS   = 24
gpio_adapter = Adafruit_GPIO_Adapter(GPIO, mode=GPIO.BOARD)
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO,mosi=MOSI, gpio=gpio_adapter)

MAXSIZE = 1000
light = [0]*MAXSIZE 
t = [0]*MAXSIZE

time_start = time.time()
cur_time = time_start
i = 0
counter = 0

while time_start + args.tim > cur_time:
  cur_time = time.time(); 
  
  if time_start + i * args.delay < cur_time:
    i = counter%MAXSIZE

    light[i] = mcp.read_adc(ADC_pin)
    t[i] = time.time() - time_start

    if DEBUG:
        print(f'Raw ADC Val: {mcp.read_adc(ADC_pin)}')
    
    counter = counter + 1

  time.sleep(0.001)

# Write data to file
file_name = f"data_DC_{args.duty}.txt"

datafile = open(file_name, "w")

for i in range(counter):
  datafile.write(f'{t[i]:0.2f}\t{light[i]:0.2f}\n')

datafile.close()

GPIO.cleanup()