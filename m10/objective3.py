import RPi.GPIO as GPIO
import argparse
import time
import cv2
import numpy as np
from picamera2 import Picamera2
import matplotlib
matplotlib.use('Pdf')
import matplotlib.pyplot as plt
import Adafruit_MCP3008
from Adafruit_GPIO.GPIO import RPiGPIOAdapter as Adafruit_GPIO_Adapter
from picar import PiCar
import mod8_func as motor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
    
# Finding angle function
def object_angle(img, debug):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (95, 100, 90), (120, 255, 255))
    mask_blur = cv2.blur(mask, (5,5))
    thresh = cv2.threshold(mask_blur, 200, 255, cv2.THRESH_BINARY)[1]

    M = cv2.moments(thresh)

    height = img.shape[0]
    width = img.shape[1]

    if M['m00'] != 0:
        
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        angle = np.arctan2(((cx-width/2)),(height-cy))
        angle = round(180 * angle/np.pi,3)

        if debug:
            print(f'Angle: {angle}\n')
            print(f'Center of Mass: {cx}, {cy}')
            img = cv2.circle(img,(cx,cy),5,(0,255,0),-1)
            img = cv2.line(img, (int(width/2),0),(int(width/2),height),(0,0,255),1)
            cv2.imwrite("CoM.jpg",img)
            
    else:
        if debug:
            print("Blue object not found in the image.")
        
        angle = 360
        cx = None
        cy = None

    return angle

# Setting arguments
parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--mock_car', action='store_true'),
parser.add_argument('--tim', type=float, default= 18.0),
parser.add_argument('--rps', type=float, default= 3.0),
parser.add_argument('--adSample', type=float, default= 0.005),
parser.add_argument('--speedCalc', type=float, default= 0.1), # being a factor of utsDelay
parser.add_argument('--adDelay', type=float, default= 0.0),
parser.add_argument('--motorDelay', type=float, default= 1.0), 
parser.add_argument('--Kp', type = float, default = 0.0),
parser.add_argument('--Ki', type = float, default = 0.0),
parser.add_argument('--Kd', type = float, default = 0.0),
parser.add_argument('--pdelay', type=float, default=0.55),
parser.add_argument('--utsdelay',type=float,default=0.05), #
parser.add_argument('--delta', type=float, default=0.1),
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()
DEBUG = False
DEBUG = args.debug

#Intializing PiCar
car = PiCar(mock_car=args.mock_car, threaded=True)

#Setting array sizes for readings
MAXSIZE = 10000
AD_reading = [0] * MAXSIZE
AD_difference = [0] * MAXSIZE
moving_avg = [0] * MAXSIZE
RPSs_act = [args.rps]*MAXSIZE 
transitions = [0]*MAXSIZE 
t = [0]*MAXSIZE

#Tracking position
i = 0
counter = 0

#RPS variables init
transitionsCount = 0
tempAD = 0
tempTrans = [0]*MAXSIZE
error = [0]*MAXSIZE
SE = 0

#Starting PWM
slope = 1/0.12 #original slope is 1/.0504
pwm = slope * args.rps 

new_pwm = 0 
print(f'Starting PWM: {pwm}')
if pwm > 100:
  pwm = 100

# Warming up motor
car.set_motor(pwm)
time.sleep(args.motorDelay)
car.set_steer_servo(0)
#car.set_swivel_servo(0)
car.set_nod_servo(0)

#Timing variables
time_start    = time.time()
cur_time      = time_start
rpsTime       = cur_time
ADTime        = cur_time
pic_time      = cur_time 
distance_time = cur_time

#Counting transitions and speed
direction = True
rps = 0
threshold = 10 

# Distance Variables
dist = 0
braked = False

# angle 
angle = 0
old_angle = angle

# Da big loop including the OBJ1 and OBJ2 (speed and angle) 
while time_start + args.tim > cur_time:

    if (cur_time - distance_time) > args.utsdelay:
        prev_dist = dist
        dist = car.read_distance()
        if dist == None: dist = prev_dist

        if dist > 60:
            if (cur_time - ADTime) > args.adSample:
                i = counter%MAXSIZE

                RPSs_act[i] = rps

                if rps > 10:
                    RPSs_act[i] = RPSs_act[i-1]
                if abs(RPSs_act[i-1] - RPSs_act[i]) > 1:
                    RPSs_act[i] = RPSs_act[i-1]

                if i > 0:
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

                if args.debug:
                    print(f'RPS: {RPSs_act[i]}')

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
                ADTime = cur_time

            if (cur_time - rpsTime) > args.speedCalc:
                count = 0
                curr_position = i
                start = 0
                end = 0

                while count < 5 and curr_position >= 0:
                
                    if transitions[curr_position] == 1:
                        if count == 0:
                            end = t[curr_position]
                            print(f'END: {end}')
                        elif count == 4:
                            start = t[curr_position]
                            print(f'START: {start}')
                            deltaTime = end - start
                            rps = 1/deltaTime
                        count += 1
                    curr_position -= 1 
                rpsTime = cur_time

        elif dist <= 60 and not braked:
            car.set_motor(75,False)
            print("yes")
            print(f"BRAKING")
            time.sleep(0.4)
            car.set_motor(0)
            # lowerEnd = -3
            # higherEnd = 3
            braked = True
        elif dist > 12:
            car.set_motor(30,True)
            print("almost")
        else:
            car.set_motor(0)
            print("stopped")
    
        if args.debug:
            print(f'distance: {dist:.2f} cm')
        distance_time = cur_time

    if (cur_time - pic_time) > args.pdelay:
        img     = car.get_image()
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        angle = object_angle(img_bgr, args.debug) / 9

        if angle == 40:
            angle = old_angle
        if angle > 10:
            angle = 10
        elif angle < -10:
            angle = -10
        else:
            angle = angle

        if abs(angle) > 2:
            car.set_steer_servo(round(angle))
        else:
            car.set_steer_servo(0)
        
        old_angle = angle

        pic_time = cur_time
        if DEBUG:
            print(f'New Angle: {angle}]\t Old Angle: {old_angle}\n')
   
    cur_time = time.time()
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
  
file_name = f'car_{args.rps}_rps.txt'

datafile = open(file_name, "w")

datafile.write(f'{args.adSample:0.4f}\n')
for i in range(counter):
  datafile.write(f'{t[i]:0.4f}\t{AD_reading[i]:0.4f}\t{RPSs_act[i]:0.4f}\n')

datafile.close()

cv2.imwrite('bgr.jpg', img_bgr)
GPIO.cleanup()

tempSum = 0
l = 0

for val in RPSs_act:
  if val > 0:
    tempSum += val
    l += 1

print(f'Average RPS: {tempSum/l}')