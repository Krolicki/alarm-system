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
#diody led
red_led = 26
green_led = 13
yellow_led = 6
GPIO.setup(red_led,GPIO.OUT)
GPIO.setup(green_led,GPIO.OUT)
GPIO.setup(yellow_led,GPIO.OUT)
#reader = mfrc522.MFRC522() #czytnik RFID
reader = SimpleMFRC522()

sensorSignal = None
isOpen = False
armed = False

def clear_led():
    GPIO.output(red_led, False)
    GPIO.output(green_led, False)
    GPIO.output(yellow_led, False)

def beep(repeat, tone): #buzzer - pętla synchronizacji fazowej
    if(tone == 'low'):
        tone = 0.000440
    elif(tone == 'hi'):
        tone = 0.000220
    else:
        tone = 0.000245
    for i in range(0, repeat):
        for pulse in range(30): 
            GPIO.output(buzzer, True)
            time.sleep(tone)
            GPIO.output(buzzer, False)
            time.sleep(tone)
        time.sleep(0.08)
        
def RFIDReader():#wątek czytnika kart
    global armed
    while True:
        id, text = reader.read()
        if(id == 977504443815):
            if not armed:
                for i in range(0, 4):
                    beep(1, "hi")
                    time.sleep(1)
                GPIO.output(red_led, True)
                GPIO.output(green_led, False)
                beep(2, "hi")
                armed = True
            else:
                beep(2, "hi")
                GPIO.output(red_led, False)
                GPIO.output(green_led, True)
                armed = False
        else:
            beep(2, "low")
            GPIO.output(yellow_led, True)
            time.sleep(2)
            GPIO.output(yellow_led, False)

#        status,TagType = reader.MFRC522_Request(reader.PICC_REQIDL)
#        status,uid = reader.MFRC522_Anticoll()
#        if status == reader.MI_OK:
#            print("UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
#            time.sleep(2)
        time.sleep(0.2)

def doorSensor(): #wątek czujnika otwarcia drzwi
    while True: 
        sensorSignal = GPIO.input(sensor)
        if(sensorSignal and (isOpen == False)):
            isOpen = True
            print("Otwarto drzwi")
            #beep(2)
        elif not (sensorSignal):
            isOpen = False

        time.sleep(0.1)

def main():
    clear_led()
    if not armed:
        GPIO.output(green_led, True)
    readerThread = Thread(target=RFIDReader)
    readerThread.start()

    #doorThread = Thread(target=doorSensor)
    #doorThread.start()
    clear_led() #tymczasowo do testów !!
    
main()