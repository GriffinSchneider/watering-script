#!/usr/bin/env python
import time
import datetime
import signal
import sys
import RPi.GPIO as GPIO
import subprocess as sp

dateString = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

print("Starting video...")

command = [ 'ffmpeg',
            '-f', 'alsa',
            '-ac', '1',
            '-i', 'plughw:1',
            '-f', 'v4l2',
            '-input_format', 'mjpeg',
            '-video_size', '1280x720', 
            '-i', '/dev/video0',
            '-c:v', 'copy',
            '-t', '00:20',
            '-nostdin',
            '-loglevel', 'error',
            'Watering_%s.avi' % dateString 
]
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

def signal_handler(signal, frame):
  print('SIGINT Received')
  GPIO.output(4, 0)
  GPIO.cleanup()
  print('Cleaned up. Exiting.')
  sys.exit(1)
signal.signal(signal.SIGINT, signal_handler)

GPIO.output(4, 0)

print("Waiting...")

time.sleep(5)

print("Watering...")

GPIO.output(4, 1)
time.sleep(5.80)
GPIO.output(4, 0)

print("Watering stopped.")
time.sleep(1)

GPIO.output(4, 0)
GPIO.cleanup()

print("Cleanup complete, waiting to finish video...")
pipe.wait()
print("Done.")
