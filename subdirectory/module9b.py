import RPi.GPIO as GPIO
import time
import argparse
from picar import PiCar

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

parser = argparse.ArgumentParser(description="Getting arguments")
parser.add_argument('--mock_car', action='store_true'),
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()
DEBUG = False
DEBUG = args.debug

car = PiCar(mock_car=args.mock_car)
MAXSIZE = 1000
time_start = time.time()
cur_time = time_start
i = 0
counter = 0
delay = 0.01
tim = 10

car.set_motor(100)
time.sleep(1)


while time_start + tim > cur_time:
  cur_time = time.time(); 

  if time_start + i * delay < cur_time:
    i = counter%MAXSIZE
    dist = car.read_distance()
    print(f'distance: {dist:.2f} cm')

    if dist > 50:
      car.set_motor(0)
    elif 45 < dist <= 50:
      car.set_motor(70)
    elif 40 < dist <= 45:
      car.set_motor(60)
    elif 35 < dist <= 40:
      car.set_motor(50)
    elif 30 < dist <= 35:
      car.set_motor(40)
    elif 25 < dist <= 30:
      car.set_motor(30)
    elif 20 < dist <= 25:
      car.set_motor(20)
    elif 15 < dist <= 20:
      car.set_motor(10)
    elif dist < 10:
      car.set_motor(0)
    else:
      car.set_motor(0)

    p0 = car.adc.read_adc(0)
    print(f'ad_0: {p0}')

    if DEBUG:
      print('Yo')

    counter = counter + 1

  time.sleep(0.001)


# datafile = open("dataWalk.txt", "w")


# for i in range(counter):
#   datafile.write(f'{distances[i]:0.2f}\t{Ax[i]:0.2f}\t{Ay[i]:0.2f}\t{Az[i]:0.2f}\t{Gx[i]:0.2f}\t{Gy[i]:0.2f}\t{Gz[i]:0.2f}\t{t[i]}\n')

# datafile.close()

GPIO.cleanup
