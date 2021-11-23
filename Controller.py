import serial
import sys
import time
import keyboard

serialPortName = "COM7" #Skal sandsynligvis ændres. Kommer an på porten som arduino sidder i.  
baudRate = 115200 #Defineret i main.cpp
fejlStop = 0 #Bruges til at programmet forsøget at finde data mere end én gang. (Vi oplevede crashes fordi at serial.readline ikke var 100% reliable)

startSend = "boop"
endSend = "poob"

s = serial.Serial(serialPortName,baudRate,timeout=1)

print("Tilslutning lavet - Venter på serial data\n")

while(True):
    if s.is_open:
        
        if keyboard.is_pressed('w'): command = "forward"
        elif keyboard.is_pressed('a'): command = "left"
        elif keyboard.is_pressed('s'): command = "backward"
        elif keyboard.is_pressed('d'): command = "right"
        else: command = "none"
            
        print(command)
        serialSend = f",{startSend},{command},{endSend},\n"
        s.write(serialSend.encode())
