from microbit import *
import music
import neopixel
import speech
import random as r

#Variabel til
LEDCOUNT = 0

# Setup the Neopixel strip on pin0 with a length of 8 pixels
np = neopixel.NeoPixel(pin15, 4)

#Kompas kalibreres (måske)
#compass.calibrate()

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

def blinkRed(n, sleepTime, pinSelected):
    for i in range(n):
        pinSelected.write_digital(0)
        sleep(sleepTime)
        pinSelected.write_digital(1)
        sleep(sleepTime)


while True:
    #Iterate over each LED in the strip
    #HER STARTER LED-SHOW
    for i in range(40):
        if LEDCOUNT == 2:
            pin8.write_digital(0)
            pin12.write_digital(1)

        for pixel_id in range(0, len(np)):
            red = r.randint(0, 60)
            green = r.randint(0, 60)
            blue = r.randint(0, 60)

            # Assign the current LED a random red, green and blue value between 0 and 60
            np[pixel_id] = (red, green, blue)

            # Display the current pixel data on the Neopixel strip
            np.show()

        if LEDCOUNT == 4:
            pin8.write_digital(1)
            pin12.write_digital(0)
            LEDCOUNT = 0


        dir=r.randint(0, 1)

        motor(dir, 255, abs(dir-1), 255)

        LEDCOUNT += 1
        sleep(100)


    pin8.write_digital(1)
    pin12.write_digital(1)
    #HER SLUTTER LED-SHOW



