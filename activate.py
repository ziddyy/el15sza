#****************General Libraries*******************
from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
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

#****************Functions*******************

def activateSystem():
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

