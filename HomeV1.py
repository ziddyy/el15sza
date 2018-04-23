#****************Libraries*******************
from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime

#****************Setup*******************
pir_1 = MotionSensor(4)
pir_2 = MotionSensor(7)

camera=PiCamera()


#****************Heart of the Code***********


while True:
    now = datetime.now()
    filename = "{0:%d}-{0:%m}-{0:%Y}.h264".format(now)
    pir_1.wait_for_motion()
    pir_2.wait_for_motion()
    print ("Intruder Alert!")
    camera.start_recording(filename)
    pir_1.wait_for_no_motion()
    pir_2.wait_for_no_motion()
    print ("Deactivated!")
    camera.stop_recording()
    
