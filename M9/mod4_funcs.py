import RPi.GPIO as GPIO
import time
import smbus		    #import SMBus module of I2C
GPIO.setwarnings(False)     # Ignore warning for now
GPIO.setmode(GPIO.BOARD)    # Use physical pin numberin

# ULTRASONIC FUNCTIONS
def ultrasonic_init(Trigger, Echo):
    # set up the input and output pins
    GPIO.setup(Trigger, GPIO.OUT)
    GPIO.output(Trigger, False)
    GPIO.setup(Echo, GPIO.IN)
    # let the sensor initialize
    time.sleep(.5)

def ultrasonic_read(Trigger, Echo):
    # trigger a reading
    GPIO.output(Trigger, True)
    time.sleep(0.00001)
    GPIO.output(Trigger, False)

    # find the start and end of the ultrasonic pulse
    while GPIO.input(Echo) == 0:
        start_time = time.time()
    while GPIO.input(Echo) == 1:
        end_time   = time.time()

    # Speed of sound 34300 cm/sec
    total_distance = (end_time - start_time) * 34300
    # Divide by 2, account for return trip for signal
    return round(total_distance/2, 1) 

#deals with the accelerometer 
def movingAvg(arr, position, numvals=3, wrap=1):
    # default to 3 pt moving average with wrap around on getting values 
    # arr       - array
    # posistion - start from this point on averages
    # numvals   - Number of values in moving average, default of 3
    # wrap      - wrap around to top or bottom of array if 1 (default), no if 0
    sumvals    = 0
    count      = 0    
    array_size = len(arr)
    # if less than numvals data, then just use what is available
    for i in range(numvals):
        # add an item to the list
        if (position - i >= 0 and position - 1 < array_size):
            sumvals = sumvals + arr[(position - i)]
            count   = count + 1
        # wrap backwards, goes to top of array, works in python
        elif (position - i < 0 and wrap == 1): 
            sumvals = sumvals + arr[(position - i)]
            count   = count + 1
        # wrap around to bottom of array with mod
        elif (position - i > array_size and wrap == 1):
            sumvals = sumvals + arr[(position - i)%array_size]
            count   = count + 1
    return sumvals/count

# ACCELEROMETER MPU-6050
# Adapted from: https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi
def MPU_Init(bus):
    Device_Address = 0x68   # MPU6050 device address
    PWR_MGMT_1     = 0x6B
    SMPLRT_DIV     = 0x19
    CONFIG         = 0x1A
    GYRO_CONFIG    = 0x1B
    INT_ENABLE     = 0x38

    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def MPU_Read(bus, val2read):
    # 1-xaccel, 2-yaccel, 3-zaccel, 4-xgyro, 5-ygyro, 6-zgyro
    #some MPU6050 Registers and their Address
    Device_Address = 0x68   # MPU6050 device address
    ACCEL_XOUT_H = 0x3B
    ACCEL_YOUT_H = 0x3D
    ACCEL_ZOUT_H = 0x3F
    GYRO_XOUT_H  = 0x43
    GYRO_YOUT_H  = 0x45
    GYRO_ZOUT_H  = 0x47

    addr = ACCEL_XOUT_H

    if (val2read == 2):
        addr = ACCEL_YOUT_H
    elif (val2read == 3):
        addr = ACCEL_ZOUT_H
    elif (val2read == 4):
        addr = GYRO_XOUT_H
    elif (val2read == 5):
        addr = GYRO_YOUT_H
    elif (val2read == 6):
        addr = GYRO_ZOUT_H

    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
    #concatenate higher and lower value
    value = ((high << 8) | low)
    #to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536
   
    if (val2read < 4):   # accel reading
        value = value/16384.0
    else:                # gyro reading
        value = value/131.0
      
    return value
