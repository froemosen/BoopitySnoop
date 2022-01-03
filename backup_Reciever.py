import radio
import random
from microbit import *
import neopixel

# The radio won't work unless it's switched on.
radio.on()
radio.config(group=42, queue=1, length=251)#Gruppe, kølængde og beskedlængde defineres
message = "none"

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


#Set awesome custom face and turn on lights
display.set_pixel(1, 0, 9)
display.set_pixel(3, 0, 9)
display.set_pixel(0, 2, 9)
display.set_pixel(4, 2, 9)
display.set_pixel(0, 3, 9)
display.set_pixel(4, 3, 9)
display.set_pixel(1, 4, 9)
display.set_pixel(2, 4, 9)
display.set_pixel(3, 4, 9)
pin8.write_digital(1)
pin12.write_digital(1)

# Setup the Neopixel strip on pin0 with a length of 8 pixels
np = neopixel.NeoPixel(pin15, 4)
for pixel_id in range(0, len(np)):
    # Assign the current LED a random red, green and blue value between 0 and 60
    np[pixel_id] = (60, 0, 0)
    # Display the current pixel data on the Neopixel strip
    np.show()


# Event loop.
while True:
    incoming = radio.receive() #Besked sendt over Radio gemmes i variabel

    if not incoming == None:
        '''
        data = incoming.split(",")

        for i in range(len(data)-2):
            if data[i] == "boop": #Sikkerhed og afkodning af besked
            message = str(data[i+1]) #Den del af beskeden som skal gemmes, gemmes i ny variabel
        '''
        message = incoming

        if "for" in message:
            motor(0, 255, 0, 255)
        elif "left" in message:
            motor(1, 50, 0, 50)
        elif "right" in message:
            motor(0, 50, 1, 50)
        elif "back" in message:
            motor(1, 100, 1, 100)
        elif "none" in message:
            motor(0, 0, 0, 0)
    #else: display.scroll(message)
