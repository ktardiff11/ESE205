import time
import argparse

# Importing matplot libraries
import matplotlib
matplotlib.use('Pdf')
import matplotlib.pyplot as plt
import numpy as np

#Importing SPI and MCP library
import RPi.GPIO as GPIO
import Adafruit_MCP3008
from Adafruit_GPIO.GPIO import RPiGPIOAdapter as Adafruit_GPIO_Adapter

# LED pin
LED_PIN = 40

# SPI configuration
CLK  = 23
MISO = 21
MOSI = 19
CS   = 24
gpio_adapter = Adafruit_GPIO_Adapter(GPIO, mode=GPIO.BOARD)
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO,mosi=MOSI, gpio=gpio_adapter)

DEBUG = True
parser = argparse.ArgumentParser(description="Read AD pins")
parser.add_argument('--times', type=int, default=10)
parser.add_argument('--period', type=int, default=4)
parser.add_argument('--AD_pin', type=int, default=0)
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()

if args.debug:
  print(f'Raw ADC Val: {mcp.read_adc(args.AD_pin)}')

i=0
p=1

# Setting up pin
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

start = time.time()
with open('data.txt', 'w') as data:

  while(i<args.times):
    GPIO.output(LED_PIN, False)
    if i == args.period*p:
      t = time.time() - start
      print(f'Light (bits): {t:0.1f}\t{mcp.read_adc(args.AD_pin)}')
      data.write(f'{t:0.1f}\t')
      data.write(f'{mcp.read_adc(args.AD_pin)}\n')

      if mcp.read_adc(args.AD_pin) < 600:
        GPIO.output(LED_PIN, True)
      p=p+1

    time.sleep(1)
    i=i+1

# Printing graph

fname = input('Enter filename: ')
file = open(fname, 'r')
data = file.read().splitlines()
MAXSIZE = len(data)

time = [0]*MAXSIZE
photo = [0]*MAXSIZE

i=0
for dat in data:
  values = dat.split()
  print(values)
  time[i] = float(values[0])
  photo[i] = int(values[1])
  i = i + 1

# Getting tick marks for x axis
xmarks = np.linspace(time[0], time[MAXSIZE-1], 5)
plt.xticks(xmarks)

plt.plot(time, photo)
plt.grid()
plt.xlabel('time - sec')
plt.ylabel('bits for Photosensor')
plt.savefig("stripe.pdf")

