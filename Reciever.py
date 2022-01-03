import radio
import random
import neopixel
from microbit import *

# The radio won't work unless it's switched on.
radio.on()
radio.config(group=42, queue=1) #Gruppe og kølængde defineres

#Turn on LEDS
pin8.write_digital(1)
pin12.write_digital(1)

#Define neopixel
np = neopixel.NeoPixel(pin15, 4)

# Assign the current LED a red, green and blue value
for pixel_id in range(0, len(np)):
    np[pixel_id] = (255, 0, 0)

# Display the current pixel data on the Neopixel strip
np.show()

# Maqueen motor control - Taget fra eksempler
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
    incoming = radio.receive() #Besked sendt over Radio gemmes i variabel

    if not incoming == None:
        #data = incoming.split(",")

        #for i in range(len(data)):
            #if data[i] == "boop" and data[i+2]== "poob": #Sikkerhed og afkodning af besked
                #message = str(data[i+1]) #Den del af beskeden som skal gemmes, gemmes i ny variabel

        message = str(incoming)

        if "forward" in message:
            motor(0, 255, 0, 255)
        elif "left" in message:
            motor(1, 100, 0, 100)
        elif "right" in message:
            motor(0, 100, 1, 100)
        elif "backward" in message:
            motor(1, 180, 1, 180)

        elif "fwdl" in message:
            motor(0, 40, 0, 255)
        elif "fwdr" in message:
            motor(0, 255, 0, 40)
        elif "bwdl" in message:
            motor(1, 20, 1, 200)
        elif "bwdr" in message:
            motor(1, 200, 1, 20)

        elif "none" in message:
            motor(0, 0, 0, 0)

        else: pass
