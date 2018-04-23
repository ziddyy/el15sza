#****************General Libraries*******************
from gpiozero import MotionSensor
from gpiozero import LED
import bluetooth
from picamera import PiCamera
from datetime import datetime
from time import sleep
import os
import sys

#****************Email Libraries*******************
import email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import email.encoders
import smtplib

#****************Setup*******************
pir_1 = MotionSensor(4)

camera=PiCamera()
led = LED(17)
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
        print("Device not in range!")
        # WAIT FOR MOTION AND THEN RECORD VIDEO
        print("Waiting for motion")
        pir_1.wait_for_motion()
        now = datetime.now()
        filename = "{0:%d}-{0:%m}-{0:%Y}.h264".format(now)
        print ("Intruder Alert!")
        camera.start_recording(filename)
        pir_1.wait_for_no_motion()
        print ("Deactivated!")
        camera.stop_recording()

        # EMAIL SETUP
        print ("PREPARTING EMAIL")
        stamp = "{0:%d}-{0:%m}-{0:%Y}.h264".format(now)
        msg = MIMEMultipart()
        msg["subject"] = stamp
        msg["from"] = "candyman959@gmail.com"
        msg["to"] = "candyman959@gmail.com"
        text = MIMEText("Intruder Alert!")
        msg.attach(text)
        print ("EMAIL PREPARED")

        # ATTACH VIDEO TO EMAIL
        print ("Attaching Video")
        attach = MIMEBase("application", "octet-stream")
        attach.set_payload(open(filename, "rb").read())
        email.encoders.encode_base64(attach)
        attach.add_header("Content-Disposition", "attachment; filename= %s" % os.path.basename(filename))
        msg.attach(attach)
        print ("Video Attached")

        #GMAIL SETUP
        print ("Gmail setting up")
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login("candyman959@gmail.com","rajtanrajtan123")
        server.sendmail("candyman959@gmail.com", "candyman959@gmail.com", msg.as_string())
        server.quit()
        print ("EMAIL SENT")
    else:
        led.on()
        print("Device detected!")
        
        
        
        
