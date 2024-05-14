
import RPi.GPIO as GPIO
import argparse
import time
import numpy as np
import matplotlib
matplotlib.use('Pdf')
import matplotlib.pyplot as plt
import Adafruit_MCP3008
from Adafruit_GPIO.GPIO import RPiGPIOAdapter as Adafruit_GPIO_Adapter
import mod8_func as motor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

ADC_pin = 0

# Defining motor pins
in1 = 35
in2 = 33
en  = 37


parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--duty', type=float, default=50.0)
parser.add_argument('--tim', type=float, default=10.0)
parser.add_argument('--adSample', type=float, default=0.005)
parser.add_argument('--speedCalc', type=float, default=0.01)
parser.add_argument('--adDelay', type=float, default=2.0)
parser.add_argument('--motorDelay', type=float, default=0.0)
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()
DEBUG = False
DEBUG = args.debug

# Init Motor
pwm_pin   = motor.motor_init(in1, in2, en, 1000, args.duty)

motor.motor_direction(in1, in2, 1)
time.sleep(args.motorDelay)

# SPI configuration
CLK  = 23
MISO = 21
MOSI = 19
CS   = 24
gpio_adapter = Adafruit_GPIO_Adapter(GPIO, mode=GPIO.BOARD)

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO,mosi=MOSI, gpio=gpio_adapter)

MAXSIZE = 10000
AD_reading = [0]*MAXSIZE
AD_difference = [0] * MAXSIZE
moving_avg = [0] * MAXSIZE

RPSs = [0]*MAXSIZE 
transitions = [0]*MAXSIZE 
t = [0]*MAXSIZE

transitionsCount = 0
tempAD = 0
tempTrans = [0]*MAXSIZE

time_start = time.time()
cur_time = time_start
rpsTime = time_start
i = 0 
counter = 0
direction = True
rps = 0
threshold = 10


while time_start + args.tim > cur_time:
  cur_time = time.time(); 
  
  if time_start + i * args.adSample < cur_time:
    i = counter%MAXSIZE
    
    # if rps < 10:
    RPSs[i] = rps
    AD_reading[i] = mcp.read_adc(ADC_pin)    
    t[i] = cur_time - time_start
    if i > 0:
      difference = AD_reading[i] - AD_reading[i-1]
      if difference < 90 and difference > -90:
        AD_difference[i] = difference
        moving_avg[i] = motor.movingAvg(AD_difference,i)

        if counter > 100:
          threshold = 0.2*(max(moving_avg) - min(moving_avg)) / 2


        if moving_avg[i] > threshold and direction:
          transitions[i] = 1
          direction = False
        if moving_avg[i] < -threshold and not direction:
          transitions[i] = 1
          direction = True

    if DEBUG:
      (f'Raw ADC Val: {mcp.read_adc(ADC_pin)}')
    counter += 1

  if rpsTime + args.speedCalc < cur_time:
    rpsTime = cur_time
    count = 0 # counter
    curr_position = i
    start = 0
    end = 0

    while count < 5 and curr_position >= 0:

      if transitions[curr_position] == 1:
        if count == 0:
          end = t[curr_position]
        elif count == 4:
          start = t[curr_position]
          deltaTime = end - start
          rps = 1/deltaTime
          
        count += 1

      curr_position -= 1 
      
    
         
  
  
  time.sleep(0.001)


if args.debug:
  fig, axs = plt.subplots(3)
  fig.suptitle('Plots')
  axs[0].plot(t, AD_reading)
  axs[1].plot(t, transitions)
  axs[2].plot(t, RPSs)

  photo = f"photo_" + str(args.duty) + "_DEBUG_plot.png"
  plt.savefig(photo)

# Write data to file
file_name = 'data_PWM_' + str(args.duty) + '.txt'

datafile = open(file_name, "w")

for i in range(counter):
  datafile.write(f'{t[i]:0.5f}\t{AD_reading[i]:0.2f}\t{transitions[i]}\t{RPSs[i]:0.2f}\n')

datafile.close()

GPIO.cleanup()

tempSum = 0
l = 0

for val in RPSs:
  if val > 0:
    tempSum += val
    l += 1

print(f'Average RPS: {tempSum/l}')