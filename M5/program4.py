import RPi.GPIO as GPIO
import argparse
import cv2
import numpy as np
from picamera2 import Picamera2
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

parser = argparse.ArgumentParser(description="Getting row and col")
parser.add_argument('--row', type=int, default=5)
parser.add_argument('--col', type=int, default=5)
args = parser.parse_args()

camera = Picamera2()
camera.start()
camera.capture_file('temp.png')

img = cv2.imread("temp.png")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
print(hsv[args.row, args.col])

