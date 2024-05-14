import time
import argparse

#Importing SPI and MCP library

import RPi.GPIO as GPIO
import Adafruit_MCP3008
from Adafruit_GPIO.GPIO import RPiGPIOAdapter as Adafruit_GPIO_Adapter

# Functions

def convert_adc2temp(val):
  c = ((val*(3.3*1000.0)/1023) - 500)/10
  f = (9.0/5.0)*c+32
  return f

def convert_adc2light(val):
  bitsOut = val * (1023/3.3)
  return bitsOut

# SPI configuration
CLK  = 23
MISO = 21
MOSI = 19
CS   = 24
gpio_adapter = Adafruit_GPIO_Adapter(GPIO, mode=GPIO.BOARD)
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI, gpio=gpio_adapter)

DEBUG = True
parser = argparse.ArgumentParser(description="Read AD pins")
parser.add_argument('--times', type=int, default=5)
parser.add_argument('--delay', type=float, default = 2)
parser.add_argument('--AD_pin0', type=int, default=0)
parser.add_argument('--AD_pin1', type=int, default=1)
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()

i=0
while(i<args.times):
  if args.debug:
    print(f'Raw ADC val: {mcp.read_adc(args.AD_pin1)}')
    print(f'Raw ADC Val: {mcp.read_adc(args.AD_pin0)}')
  print(f'Degrees F: {convert_adc2temp(mcp.read_adc(args.AD_pin1))}')
  print(f'Light (bits): {mcp.read_adc(args.AD_pin0)}')
  time.sleep(args.delay)
  i=i+1
