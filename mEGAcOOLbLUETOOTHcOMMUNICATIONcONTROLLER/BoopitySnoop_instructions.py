from microbit import *
import music
import neopixel

# Maqueen motor control
# direction:0=forward  1=back
# speed：0~255
I2caddr = 0x10
def motor(directionL, speedL, directionR, speedR):
    buf = bytearray(5)
    buf[0] = 0x10
    buf[1] = directionL
    buf[2] = speedL
    buf[3] = directionR
    buf[4] = speedR
    i2c.write(I2caddr, buf)

def blinkRed(n, sleepTime, pinSelected):
    for i in range(n):
        pinSelected.write_digital(0)
        sleep(sleepTime)
        pinSelected.write_digital(1)
        sleep(sleepTime)

#https://microbit-micropython.readthedocs.io/en/v1.0.1/uart.html
uart.init(baudrate=9600, bits=8)

while True:
    if uart.any():
        display.scroll(uart.read([nbytes]))

    blinkRed(3, 500, pin8)
    blinkRed(3, 500, pin12)
