import RPi.GPIO as GPIO
import argparse
import cv2
import numpy as np
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

img = cv2.imread("selfie.jpg")

parser = argparse.ArgumentParser(description="Getting width")
parser.add_argument('--width', type=int, default=5)
args = parser.parse_args()

img_resized = cv2.resize(img, (args.width, img.shape[0]), interpolation = cv2.INTER_AREA)

cv2.imwrite('Original.jpg', img)
cv2.imwrite('Original_resized.jpg', img_resized)
