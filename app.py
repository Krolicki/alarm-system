import RPi.GPIO as GPIO
import time
from threading import Thread
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

sensor = 12 #pin GPIO czujnika otwarcia drzwi
GPIO.setup(sensor, GPIO.IN, pull_up_down = GPIO.PUD_UP) #sygnał wejściowy + pull-up na 1
buzzer = 4 #pin GPIO buzzera
GPIO.setup(buzzer,GPIO.OUT)
czujnik = 18 #czujnik ruchu
GPIO.setup(czujnik,GPIO.IN)

#diody led
red_led = 26
green_led = 13
yellow_led = 6
GPIO.setup(red_led,GPIO.OUT)
GPIO.setup(green_led,GPIO.OUT)
GPIO.setup(yellow_led,GPIO.OUT)

reader = SimpleMFRC522() #czytnik kart

sensorSignal = None
isOpen = False
armed = False
alarming = False

def clear_led(): #wyłączanie wszystkich diód LED
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

def alarm(): #dźwięk alarmu
    #for i in range(0, 10):
    while True:
        for pulse in range(30): 
            GPIO.output(buzzer, True)
            time.sleep(0.000200)
            GPIO.output(buzzer, False)
            time.sleep(0.000200)
        #global isOpen
        global armed
        if not armed: #wyłączenie alarmu po rozbrojeniu systemu
            break
        #elif not isOpen: #wyłączenie alarmu po zamknięcu drzwi 
        #    break
        else:
            time.sleep(0.3)

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
                doorThread = Thread(target=doorSensor)
                doorThread.start()
                motionThread = Thread(target=motion)
                motionThread.start()
            else:
                armed = False
                beep(2, "hi")
                GPIO.output(red_led, False)
                GPIO.output(green_led, True)
                time.sleep(2)
        else:
            beep(2, "low")
            GPIO.output(yellow_led, True)
            time.sleep(2)
            GPIO.output(yellow_led, False)
        time.sleep(0.2)

def doorSensor(): #wątek czujnika otwarcia drzwi
    while True:
        global alarming
        global isOpen
        sensorSignal = GPIO.input(sensor)
        if sensorSignal and not isOpen:
            isOpen = True
            print("Otwarto drzwi")
            if not alarming:
                alarmThread = Thread(target=alarm)
                alarmThread.start()
                alarming = True
            break
        elif not (sensorSignal):
            isOpen = False
        global armed
        if not armed:
            break
        else:
           time.sleep(0.1) 

def motion(): #wątek czujnika ruchu
    detect = 0
    while True:
        global alarming
        motionSignal=GPIO.input(18)
        if motionSignal==1:
            detect += 1
            if detect == 3 and not alarming:
                alarmThread = Thread(target=alarm)
                alarmThread.start()
                alarming = True
            time.sleep(1)
        global armed
        if not armed:
            break
        else:
            time.sleep(0.1)

def main():
    clear_led()
    if not armed:
        GPIO.output(green_led, True)
    readerThread = Thread(target=RFIDReader)
    readerThread.start()
    #clear_led() #tymczasowo do testów !!
main()