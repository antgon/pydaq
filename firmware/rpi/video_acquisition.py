# initialise resolution and framerate in constuctor
# use wait_for_edge to trigger video

# import picamera
# with picamera.PiCamera() as camera:
#     for filename in camera.record_sequence(
#             'clip%02d.h264' % i for i in range(3)):
#         print('Recording to %s' % filename)
#         camera.wait_recording(10)

import time
import datetime as dt
import picamera
import RPi.GPIO as GPIO

bcm_pin = 23 # This is the 8th pin on the external row. Physical eq is 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(bcm_pin, GPIO.IN, GPIO.PUD_DOWN)

# The pin input is normally up because of input from mbed. Mbed pulls
# down this pin to trigger video capture.

camera = picamera.PiCamera(resolution=(640, 480))
time.sleep(2)

def mkfname():
    now = dt.datetime.now()
    return now.strftime('%Y-%m-%dT%H%M%S.h264')

# so - each video is 30 min long = 1800 seconds

GPIO.add_event_detect(bcm_pin, GPIO.BOTH)
if GPIO.event_detected(bcm_pin):
    if GPIO.input(bcm_pin) == GPIO.LOW:
        camera.start_recording(mkfname())
        camera.start_preview()
        camera.wait_recording(10)
        while True:
            camera.split_recording(mkfname())
            camera.wait_recording(10)
    else:
        camera.stop_recording()
        camera.stop_preview()

GPIO.cleanup()
