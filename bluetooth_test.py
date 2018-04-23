import bluetooth
from gpiozero import LED
from time import sleep


search_time = 10
led = LED(17)
addr = "bc:76:5e:17:0b:7c" #None allows the script to run discover devices. Devices can be hardcoded to skip discovery part

print("Bluetooth Search \nEnsure bluetooth is switched on and made discoverable.")

if addr == None:
    try:
        input("Press the Enter key to begin the search")
    except SyntaxError:
        pass

    print("Searching for devices....")

    nearby_devices = bluetooth.discover_devices(duration=search_time, flush_cache=True, lookup_names=True)

    if len(nearby_devices) > 0:
        print("Found %d devices!" % len(nearby_devices))
    else:
        print("Device not found. Restart script and try again")
        exit(0)

    i = 0 #Increments the list of devices found
    # Prints out devices found
    for addr, name in nearby_devices:
        print("%s. %s - %s" % (i, addr, name))
        i =+ 1

    device_num = input("Which device number do you want to connect to?")

    # save the useful information we need from the device
    addr, name = nearby_devices[device_num][0], nearby_devices[device_num][1]

print("The script will now scan for the device %s." % (addr))
print("\nUse Ctrl+c to exit")

while True:
    # Try to gather information from the desired device.
    # We're using two different metrics (readable name and data services)
    # to reduce false negatives.
    state = bluetooth.lookup_name(addr, timeout=20)
    services = bluetooth.find_service(address=addr)
    # Flip the LED pin on or off depending on whether the device is nearby
    if state == None and services == []:
        print("Device not in range!")
        led.off()
    else:
        print("Device detected!")
        led.on()
        sleep(1)
