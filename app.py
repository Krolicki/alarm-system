import RPi.GPIO as GPIO
import time
from threading import Thread
#import mfrc522 #RFID
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

sensor = 12 #pin GPIO czujnika otwarcia drzwi
GPIO.setup(sensor, GPIO.IN, pull_up_down = GPIO.PUD_UP) #sygnał wejściowy + pull-up na 1
buzzer = 4 #pin GPIO buzzera
GPIO.setup(buzzer,GPIO.OUT)
#reader = mfrc522.MFRC522() #czytnik RFID
reader = SimpleMFRC522()

sensorSignal = None
isOpen = False

def beep(repeat): #buzzer - pętla synchronizacji fazowej
   for i in range(0, repeat):
      for pulse in range(30):
         GPIO.output(buzzer, True)
         time.sleep(0.000245)
         GPIO.output(buzzer, False)
         time.sleep(0.000245)
      time.sleep(0.08)
      
def RFIDReader(): #wątek czytnika kart
     while True:
        id, text = reader.read()
        if(id == 977504443815):
             beep(1)
             time.sleep(2)
#        status,TagType = reader.MFRC522_Request(reader.PICC_REQIDL)
#        status,uid = reader.MFRC522_Anticoll()
#        if status == reader.MI_OK:
#            print("UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
#            time.sleep(2)
        time.sleep(0.1)

def doorSensor(): #wątek czujnika otwarcia drzwi
    while True: 
        sensorSignal = GPIO.input(sensor)
        if(sensorSignal and (isOpen == False)):
            isOpen = True
            print("Otwarto drzwi")
            beep(2)
        elif not (sensorSignal):
            isOpen = False

        time.sleep(0.1)

def main():

    readerThread = Thread(target=RFIDReader)
    readerThread.start()

    doorThread = Thread(target=doorSensor)
    doorThread.start()

    
main()