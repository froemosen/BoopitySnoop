from keras.models import load_model #pip install keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import time
import serial
import sys

#Load the model
model = load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

#Load camera
camera = cv2.VideoCapture(1)#0-front, 1-rear
ret, blackImage = camera.read()
ret, blackImage = camera.read()
ret, blackImage = camera.read()
cv2.waitKey(1)
time.sleep(3)

#Setup af serial
serialPortName = "COM7" #Skal sandsynligvis ændres. Kommer an på porten som micro:bit sidder i. Dette kan tjekkes på windows under "endhedshåndtering" 
baudRate = 115200 #Standard baud-rate for micro:bit

startSend = "boop" #Kodeord for at andre personer ikke benytter samme UART-kanal
endSend = "poob" #Bruges til at markere afslutning på besked



try:
    s = serial.Serial(serialPortName,baudRate,timeout=1)
    print("Tilslutning lavet - Afventer sending af serial data\n")
except:
    print("Kunne ikke sende data gennem", serialPortName, "Husk at tjekke hvilket port micro:bit kører igennem")
    sys.exit(1) #Lukker programmet

def get_image(): #Tager billede fra kamera, og ændrer det til rgb-format
    retval, image = camera.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imshow("image", image) #Viser video-feed
    cv2.waitKey(1) #Sørger for at video-feed ikke crasher programmet
    image = Image.fromarray(image)
    return image

def predict():
    image = get_image()

    #resize the image to a 224x224 with the same strategy as in TM2:
    #image = np.array(cap)
    #resizing the image to be at least 224x224 and then cropping from the center        
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    #normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    return np.argmax(prediction)
    
def sendSerial(command):
        if s.is_open:
            print(command)
            serialSend = f",{startSend},{command},{endSend},\n"
            s.write(serialSend.encode())
    
categories=["none","left","right","backward","forward"]

if __name__ == '__main__':
    while True:
        command = (categories[predict()])
        print(command)
        sendSerial(command)
        
    