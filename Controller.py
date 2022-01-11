import serial
import sys
import time
import keyboard
import random as r

serialPortName = "COM7" #Skal sandsynligvis ændres. Kommer an på porten som arduino sidder i.  
baudRate = 115200 #Defineret i main.cpp
fejlStop = 0 #Bruges til at programmet forsøget at finde data mere end én gang. (Vi oplevede crashes fordi at serial.readline ikke var 100% reliable)

#startSend = "boop"
#endSend = "poob"

try:
    s = serial.Serial(serialPortName,baudRate,timeout=1)
except:
    print("Kunne ikke finde data gennem", serialPortName, "Husk at tjekke hvilket port arduino kører igennem")
    sys.exit(1)

print("Tilslutning lavet - Venter på serial data\n")

def secure(key):
    code = (key*27%123456*42+147+key)%999
    return code

while(True):
    try:
        if s.is_open:
            
            if keyboard.is_pressed('w') and keyboard.is_pressed('a'): command = "q" #"fwdl"
            elif keyboard.is_pressed('w') and keyboard.is_pressed('d'): command = "e" #"fwdr"
            elif keyboard.is_pressed('s') and keyboard.is_pressed('a'): command = "z" #"bwdl"
            elif keyboard.is_pressed('s') and keyboard.is_pressed('d'): command = "c" #"bwdr"
            elif keyboard.is_pressed('w'): command = "w" #"forward"
            elif keyboard.is_pressed('a'): command = "a" #"left"
            elif keyboard.is_pressed('s'): command = "s" #"backward"
            elif keyboard.is_pressed('d'): command = "d" #"right"
            else: command = "n" #"none"

            
            print(command)

            #Secure message
            key0 = r.randint(45, 126) #81 ascii-karakterer som ikke er et komma - Giver 81^2*8 (52.488) forskellige kombinationer
            key1 = r.randint(45, 126)
            unix = str(round(time.time()%1000, 2)).replace(".", "")
            key = int(str(key0)+str(key1)+str(ord(command))+unix)
            charKey0 = chr(key0)
            charKey1 = chr(key1)
            code = secure(key)
            command = f",{charKey0+charKey1},{command},{code},{unix},"
            #print(key)
            print(command)
            print(key)

            #End message
            command+='\r\n'
            
            #serialSend = f",{startSend},{command},{endSend},"
            #s.write(serialSend.encode())
            s.write(command.encode())

            time.sleep(0.01)
    except: print("Failure, STOP MESSING WITH ME")
        

