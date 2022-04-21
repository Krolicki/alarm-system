import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

sensor = 12 #pin GPIO czujnika otwarcia drzwi
GPIO.setup(sensor, GPIO.IN, pull_up_down = GPIO.PUD_UP) #sygnał wejściowy + pull-up na 1
buzzer = 4 #pin GPIO buzzera
GPIO.setup(buzzer,GPIO.OUT)

sensorSignal = None
isOpen = False

def beep(repeat): #buzzer - pętla synchronizacji fazowej
   for i in range(0, repeat):
      for pulse in range(60):
         GPIO.output(buzzer, True)
         time.sleep(0.0001704)
         GPIO.output(buzzer, False)
         time.sleep(0.0001704)
      time.sleep(0.05)
 

while True: #główna pętla
    sensorSignal = GPIO.input(sensor)
    if(sensorSignal and (isOpen == False)):
        beepThread = threading.Thread(target=beep(3), args=(0,))
        beepThread.start()
        isOpen = True
        print("Otwarto drzwi")
        #beep(3)
    elif not (sensorSignal):
        isOpen = False

    time.sleep(0.1)