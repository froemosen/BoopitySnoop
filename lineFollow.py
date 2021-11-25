# Line-tracking Maqueen
# @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)

from microbit import *
I2caddr = 0x10

# Maqueen motor control
# direction:0=forward  1=back
# speed：0~255
def motor(directionL, speedL, directionR, speedR):
    buf = bytearray(5)
    buf[0] = 0x00
    buf[1] = directionL
    buf[2] = speedL
    buf[3] = directionR
    buf[4] = speedR
    i2c.write(I2caddr, buf)

# index：the corresponding line-tracking sensor
def Patrol(index):
    if(index == 1):
        a = pin13.read_digital()
        return a
    if(index == 2):
        a = pin14.read_digital()
        return a

while True:
    # When the left and right line-tracking sensors are not on the black line
    if Patrol(1) == 0 and Patrol(2) == 0:
        motor(0, 200, 0, 200)
    # When the left line-tracking sensors is on the black line
    elif Patrol(1) == 1 and Patrol(2) == 0:
        motor(0, 255, 0, 50)
    # When the right line-tracking sensors is on the black line
    elif Patrol(1) == 0 and Patrol(2) == 1:
        motor(0, 50, 0, 255)
