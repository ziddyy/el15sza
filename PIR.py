import RPi.GPIO as GPIO                 #Import the GPIO library
import time                             #Import the Time library

GPIO.setmode(GPIO.BCM)                  #Broadcom pin numbering

PIR_ONE = 7                             #Define the PIR sensor pin
GPIO.setup(PIR_ONE, GPIO.IN)            #Define PIR pin as input pin

try:                                    #Try loop so we know our system is ready
    print ("System Activating (CTRL+C to exit)")
    time.sleep(2)
    print ("Activated")

    while True:                         #Check status of PIR_ONE
        if GPIO.input(PIR_ONE):
            print ("Intruder Alert!")
        time.sleep(1)
except KeyboardInterrupt:               #Clean up to exit 
    print ("Deactivated")
    GPIO.cleanup()
