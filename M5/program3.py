import RPi.GPIO as GPIO
import argparse
import cv2
import numpy as np
from picamera2 import Picamera2
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# b
camera = Picamera2()
camera.start()
camera.capture_file('testing1.png')

# c
img = cv2.imread("testing1.png")
print(img.size)
print(img.shape)

 # E
new_width = int(img.shape[1]/2)
new_height = int(img.shape[0]/2)
smaller = cv2.resize(img, (new_width, new_height), interpolation = cv2.INTER_AREA)
cv2.imwrite('small_testing1.png', smaller)

# G
# Changing from BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# 1st set of values (27, 150, 150) form lower limits, the second the upper
mask = cv2.inRange(hsv, (27, 10, 10), (33, 255, 255))
# H
M = cv2.moments(mask)
cXM = int(M["m10"] / M["m00"])
cYM = int(M["m01"] / M["m00"])
print (f"Center: ({cXM}, {cYM})")

mask_blur = cv2.blur(mask, (5,5))

thresh = cv2.threshold(mask_blur, 150, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('testing_thresh.png', thresh)
M = cv2.moments(thresh)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
print (f"Center: ({cX} , {cY})")

img = cv2.circle(img, (cXM,cYM), 5, (255,0,0), 2) # blue circle
img = cv2.circle(img, (cX,cY), 5, (0,255,0), 2) # green circle
cv2.imwrite('yellow_testing.png', img)

