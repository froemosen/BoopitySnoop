import radio
import random
from microbit import *
import speech

# The radio won't work unless it's switched on.
radio.on()
radio.config(group=42, queue=1)

# Maqueen motor control
# direction:0=forward  1=back
# speed：0~255
I2caddr = 0x10
def motor(directionL, speedL, directionR, speedR):
    buf = bytearray(5)
    buf[0] = 0x00
    buf[1] = directionL
    buf[2] = speedL
    buf[3] = directionR
    buf[4] = speedR
    i2c.write(I2caddr, buf)

# Event loop.
while True:
    incoming = radio.receive()

    if not incoming == None:
        data = incoming.split(",")

        for i in range(len(data)):
            if data[i] == "boop":
                message = str(data[i+1])


        if message == "forward":
            motor(0, 255, 0, 255)
        elif message == "left":
            motor(1, 50, 0, 50)
        elif message == "right":
            motor(0, 50, 1, 50)
        elif message == "backward":
            motor(1, 100, 1, 100)
        elif message == "none":
            motor(0, 0, 0, 0)
        else: pass
