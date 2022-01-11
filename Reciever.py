import radio
import random
import neopixel
from microbit import *

# The radio won't work unless it's switched on.
radio.on()
radio.config(group=42, queue=1) #Gruppe og kølængde defineres

#Show power level


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

#Time bools:
timeHigh = False
timeOK = False
prevTime = 0

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

#Security check - Selv udarbejdet.
def secure(recieved):
    global prevTime
    data = recieved.split(",")

    key = ""

    for char in data[1]:
        key += str(ord(char))

    key += str(ord(data[2]))
    key += str(int(data[4]))

    #print(key)
    #print(str(ord(data[2])))

    key = int(key)

    #display.scroll(str(key))
    time = int(data[4])

    if time > 999000:
        timeHigh = True
    else:
        timeHigh = False

    if prevTime <= time:
        timeOK = True
    elif timeHigh or time < 200:
        timeOK = True
    else:
        timeOK = False

    prevTime = time
    #display.scroll(str((key*27%123456*42+147+key)%999))

    code = int(data[3])

    if code == (key*27%123456*42+147+key)%999 and timeOK: return (True, str(data[2]))
    else: return (False, str(data[2]))



# Event loop
while True:
    incoming = radio.receive() #Besked sendt over Radio gemmes i variabel
    message = str(incoming)

    if not incoming == None:
        try: security, command = secure(message)
        except: security = False

        if security:
            if "w" in command: #"forward"
                motor(0, 255, 0, 255)
            elif "a" in command: #"left"
                motor(1, 100, 0, 100)
            elif "d" in command: #"right"
                motor(0, 100, 1, 100)
            elif "s" in command: #"backward"
                motor(1, 180, 1, 180)

            elif "q" in command: #"fwdl"
                motor(0, 40, 0, 255)
            elif "e" in command: #"fwdr"
                motor(0, 255, 0, 40)
            elif "z" in command: #"bwdl"
                motor(1, 200, 1, 20)
            elif "c" in command: #"bwdr"
                motor(1, 20, 1, 200)

            elif "n" in command: #"none"
                motor(0, 0, 0, 0)

            else: pass
        else: pass
    else: pass

