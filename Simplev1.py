#****************General Libraries*******************
import bluetooth
from time import sleep
from gpiozero import LED
from activate import activateSystem

#****************Email Libraries*******************

#****************Setup*******************
led = LED(17)

#****************Functions*******************

addr = "bc:76:5e:17:0b:7c" #None allows the script to run discover devices. Devices can be hardcoded to skip discovery part

print("Bluetooth Search \nEnsure bluetooth is switched on and made discoverable.")
while True:
    # Try to gather information from the desired device.
    # We're using two different metrics (readable name and data services)
    # to reduce false negatives.
    state = bluetooth.lookup_name(addr, timeout=20)
    services = bluetooth.find_service(address=addr)
    #Arm/Disarm System
    if state == None and services == []:
        print("User is not within range")
        activateSystem()
    else:
        led.on()
        print("Device detected!")
