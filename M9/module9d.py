import RPi.GPIO as GPIO
import argparse
import cv2
import time
import numpy as np
from picamera2 import Picamera2
from picar import PiCar
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Finding angle function
def object_angle(img, debug):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    mask = cv2.inRange(hsv, (100, 50, 50), (130, 255, 255))

    M = cv2.moments(mask)

    if M['m00'] > 0:

        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        mask_blur = cv2.blur(mask, (5,5))
        
        thresh = cv2.threshold(mask_blur, 150, 255, cv2.THRESH_BINARY)[1]
        M = cv2.moments(thresh)


        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        angle = np.degrees(np.arctan2(((img.shape[1]/2)-cx),(img.shape[0] -cy)))

        if debug:
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)

            cv2.imwrite('Mask.jpg', mask)

            cv2.imwrite('CoM.jpg', img)
            
            print(f'Angle: {angle}\n')
            print(f'Center of Mass: {cx}, {cy}')
            

        return angle
    else:
        if debug:
            print("Blue object not found in the image.")
        return 360  


camera = Picamera2()
camera.start()
camera.capture_file('testing1.png')


parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--tim', type=int, default=10)
parser.add_argument('--mock_car', action='store_true')
parser.add_argument('--delay', type=float, default=0.5)
parser.add_argument('--delta', type=float, default=0.25)
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()
DEBUG = False
DEBUG = args.debug

car = PiCar(mock_car=args.mock_car)

car.configure_swivel_servo_positions (-10, 0, 10)

car.set_swivel_servo(8.5)
time.sleep(1) 

time_start = time.time()
cur_time = time_start
i = 0

pwmAngle = 20 / (180-0)
newPWM = 7.5
oldPWM = newPWM

while time_start + args.tim > cur_time:
  cur_time = time.time(); 

  if time_start + i * args.delay < cur_time:

    camera.capture_file('track.png')
    img = cv2.imread('track.png')
    img = cv2.flip(img,-1)
    angle = object_angle(img, DEBUG)

    if angle <= 90 and angle >= -90:
        newPWM = oldPWM + angle*args.delta*pwmAngle

    if newPWM < -10:
      newPWM = -10

    if newPWM > 10:
      newPWM = 10

    if DEBUG:
      print(f'New PWM: {newPWM} \t Old PWM: {oldPWM} \t Angle: {angle}')

    if -10 <= newPWM and 10 >= newPWM:
      car.set_swivel_servo(newPWM)
      time.sleep(1)
    
      
    else:
       newPWM = 7.5
       car.set_swivel_servo(newPWM)
       time.sleep(1)
    
    oldPWM = newPWM

    i+=1
    time.sleep(0.001)

GPIO.cleanup()