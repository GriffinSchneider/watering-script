#!/usr/bin/env python
import time
import datetime
import signal
import sys
import RPi.GPIO as GPIO
import subprocess as sp

dateString = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

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
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

GPIO.output(4, 0)

time.sleep(5)

GPIO.output(4, 1)
time.sleep(5.80)
GPIO.output(4, 0)

GPIO.output(4, 0)
GPIO.cleanup()

pipe.wait()
