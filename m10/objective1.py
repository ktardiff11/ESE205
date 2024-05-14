import RPi.GPIO as GPIO
import argparse
import time
import numpy as np
import matplotlib
matplotlib.use('Pdf')
import matplotlib.pyplot as plt
import Adafruit_MCP3008
from Adafruit_GPIO.GPIO import RPiGPIOAdapter as Adafruit_GPIO_Adapter
from picar import PiCar
import mod8_func as motor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--rps', type=float, default= 3.0)
parser.add_argument('--tim', type=float, default= 10.0)
parser.add_argument('--adSample', type=float, default= 0.005)
parser.add_argument('--speedCalc', type=float, default= 0.1)
parser.add_argument('--adDelay', type=float, default= 2.0)
parser.add_argument('--motorDelay', type=float, default= 0.0)
parser.add_argument('--debug', action='store_true')
parser.add_argument('--Kp', type = float, default = 0.0)
parser.add_argument('--Ki', type = float, default = 0.0)
parser.add_argument('--Kd', type = float, default = 0.0)
parser.add_argument('--mock_car', action='store_true')

args = parser.parse_args()
DEBUG = False
DEBUG = args.debug


car = PiCar(mock_car=args.mock_car)

MAXSIZE = 10000
AD_reading = [0] * MAXSIZE
AD_difference = [0] * MAXSIZE
moving_avg = [0] * MAXSIZE

RPSs_act = [args.rps]*MAXSIZE 
transitions = [0]*MAXSIZE 
t = [0]*MAXSIZE

transitionsCount = 0
tempAD = 0
tempTrans = [0]*MAXSIZE
error = [0]*MAXSIZE
SE = 0

time_start = time.time()
cur_time = time_start
rpsTime = time_start
i = 0 
counter = 0
direction = True
rps = 0
threshold = 10 

slope = 1/0.12 #original slope is 1/.0504
pwm = slope * args.rps 

new_pwm = 0 

print(pwm)
if pwm > 100:
  pwm = 100

car.set_motor(pwm)
time.sleep(args.motorDelay)


while time_start + args.tim > cur_time:
  cur_time = time.time(); 
  
 

  if time_start + i * args.adSample < cur_time:
    i = counter%MAXSIZE

    RPSs_act[i] = rps


    if rps > 10:
      RPSs_act[i] = RPSs_act[i-1]
      if abs(RPSs_act[i-1] - RPSs_act[i]) > 1:
        RPSs_act[i] = RPSs_act[i-1]


    if i > 0:
      print(f'RPS: {RPSs_act[i]}')
      error[i] = args.rps - RPSs_act[i] 
      derivError = error[i] - error[i-1]
      SE += error[i]
      errorKp = error[i] * args.Kp 
      errorKi = SE * args.Ki
      errorKd = 0
      new_pwm = (args.rps * slope) + (errorKp + errorKi + errorKd)
      

      if new_pwm > 100:
        new_pwm = 100
      
      elif new_pwm < 0:
        new_pwm = pwm 
        
      elif new_pwm > 0 and new_pwm < 20:
        new_pwm = 25
        pwm = new_pwm
        car.set_motor(new_pwm)
      

    tempAD = car.adc.read_adc(0)
    AD_reading[i] = tempAD
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
      print(f'Raw ADC Val: {car.adc.read_adc(0)}')
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
  axs[2].plot(t, RPSs_act)

  photo = f"photob_" + str(args.rps) + "_DEBUG_plot.png"
  plt.savefig(photo)

# Write data to file
  
file_name = 'car_noload_5rps.txt'

datafile = open(file_name, "w")

datafile.write(f'{args.adSample:0.4f}\n')
for i in range(counter):
  datafile.write(f'{t[i]:0.4f}\t{AD_reading[i]:0.4f}\t{RPSs_act[i]:0.4f}\n')

datafile.close()

GPIO.cleanup()

tempSum = 0
l = 0

for val in RPSs_act:
  if val > 0:
    tempSum += val
    l += 1

print(f'Average RPS: {tempSum/l}')