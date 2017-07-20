#! /usr/bin/env	python3
import time
import datetime as dt
import picamera
import RPi.GPIO as GPIO
import threading
import sys

# The pin input is normally up because of input from mbed. Mbed pulls
# down this pin to trigger video capture.
bcm_pin = 23 # This is the 8th pin on the external row. Physical eq is 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(bcm_pin, GPIO.IN, GPIO.PUD_DOWN)

resolution = (640, 480) # (1296,972)
#framerate = None #25
video_len = 1800 # length in seconds of each video.
# zoom: x, y, w, h (range 0.0 to 1.0)
zoom = (0.32, 0.23, 0.47, 0.47)

def mkfname():
    now = dt.datetime.now()
    return now.strftime('%Y-%m-%dT%H%M%S.h264')

class Capture():
    def __init__(self, camera=None):
        self.camera = picamera.PiCamera(resolution=resolution)
        self.camera.zoom = zoom
        self.do_run = False
        time.sleep(2)

    def start(self):
        if self.do_run is True:
            return
        self.do_run = True
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def _run(self):
        self.camera.start_preview()
        self.camera.start_recording(mkfname(), format='h264')
        while self.do_run:
            self.camera.wait_recording(video_len) # wait in seconds
            self.camera.split_recording(mkfname())

    def stop(self):
        if self.do_run is False:
            return
        self.do_run = False
        try:
            self.camera.stop_recording()
        except picamera.exc.PiCameraNotRecording:
            pass
        self.camera.stop_preview()
        self._thread.join()

def mycallback(channel):
    global capture
    if GPIO.input(bcm_pin) == GPIO.LOW:
        capture.start()
    else:
        capture.stop()

capture = Capture()
GPIO.add_event_detect(bcm_pin, GPIO.BOTH, callback=mycallback)

try:
    print("Running. Press CTRL+C to quit.")
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("\nClosing down... ", end="")
    capture.stop()
    capture.camera.close()
    GPIO.cleanup()
    print("done.")
    sys.exit()
    

