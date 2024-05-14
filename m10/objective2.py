import RPi.GPIO as GPIO
import time
import argparse
import cv2
import numpy as np
from picamera2 import Picamera2
from picar import PiCar
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

parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--mock_car', action='store_true'),
parser.add_argument('--debug', action='store_true')
parser.add_argument('--pdelay', type=float, default=0.55),
parser.add_argument('--utsdelay',type=float,default=0.1)
parser.add_argument('--delta', type=float, default=0.1)
parser.add_argument('--tim', type=float, default=10)


args = parser.parse_args()
DEBUG = False
DEBUG = args.debug

car = PiCar(mock_car=False,threaded=True)

time_start = time.time()
cur_time = time_start

angle = 0
old_angle = angle

picDelay = .5

lowerEnd = -10
higherEnd = 10

car.set_motor(25)
car.set_steer_servo(0)
#car.set_swivel_servo(0)
car.set_nod_servo(0)

dist = 0

braked = False

distance_time = cur_time
pic_time = cur_time

while time_start + args.tim > cur_time:
  

  # print(f'Ultrasonic: {time_start - cur_time}')

  if (cur_time - distance_time) > args.utsdelay:
    prev_dist = dist
    dist = car.read_distance()
    if dist == None: dist = prev_dist

    if dist > 60:
      car.set_motor(75,True)
      # print(f"starting speed")
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
      
    if DEBUG: print(f'distance: {dist:.2f} cm')
    
    distance_time = cur_time

  
  if (cur_time - pic_time) > args.pdelay:
    #print("Taking picture")
    img = car.get_image()
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # Feed a color convert into the angle image 
    # RBG to BGR then

    angle = object_angle(img_bgr,args.debug)/9


    if angle == 40:
      angle = old_angle
    # else:
    #   angle = old_angle + args.delta*angle

    if angle > higherEnd:
      angle = higherEnd
    elif angle < lowerEnd:
      angle = lowerEnd
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

cv2.imwrite('bgr.jpg', img_bgr)
GPIO.cleanup
