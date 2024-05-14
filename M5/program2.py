import RPi.GPIO as GPIO
import argparse
import cv2
import numpy as np
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

img = cv2.imread("selfie.jpg")

height = img.shape[0]
width = img.shape[1]

scale = min(200/height, 200/width)

new_h = int(scale * height)
new_w = int(scale * width)

img_resized = cv2.resize(img, (new_w, new_h), interpolation = cv2.INTER_AREA)

cv2.imwrite('Orginal_thmb.jpg', img_resized)
