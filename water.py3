#!/usr/bin/env python
import time
import datetime
import signal
import sys
import RPi.GPIO as GPIO
import subprocess as sp

dateString = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

firstTime =  34
secondTime = 30
videoTime = '01:15'

def start_video():
  command = [ 'ffmpeg',
              '-f', 'alsa',
              '-ac', '1',
              '-i', 'plughw:1',
              '-f', 'v4l2',
              '-input_format', 'mjpeg',
              '-video_size', '1280x720', 
              '-i', '/dev/video0',
              '-c:v', 'copy',
              '-t', videoTime,
              '-nostdin',
              '-loglevel', 'error',
              'Watering_%s.avi' % dateString 
  ]
  return sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

print("Starting video...")
pipe = None
while not pipe:
  maybePipe = start_video()
  time.sleep(1)
  print(maybePipe.poll())
  if maybePipe.poll() is None:
    print("Video start success.")
    pipe = maybePipe
  else:
    print("Video start failed. Retrying.")
    time.sleep(10)


GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

def signal_handler(signal, frame):
  print('SIGINT Received')
  GPIO.output(4, 0)
  GPIO.output(26, 0)
  GPIO.cleanup()
  print('Cleaned up. Exiting.')
  pipe.wait()
  sys.exit(1)
signal.signal(signal.SIGINT, signal_handler)

GPIO.output(4, 0)
GPIO.output(26, 0)

print("Waiting...")

time.sleep(5)

try:
  print("Watering 1...")
  GPIO.output(4, 1)
  time.sleep(firstTime)
  GPIO.output(4, 0)
  print("Watering 1 stopped.")

  time.sleep(1)
  GPIO.output(4, 0)
  GPIO.output(26, 0)

  print("Watering 2...")
  GPIO.output(26, 1)
  time.sleep(secondTime)
  GPIO.output(26, 0)
  print("Watering 2 stopped.")

  time.sleep(1)
  GPIO.output(4, 0)
  GPIO.output(26, 0)

  GPIO.cleanup()

  print("Cleanup complete, waiting to finish video...")
  pipe.wait()
  print("Done.")
except Exception:
  print("CAUGHT EXCEPTION:", sys.exc_info()[0])
  GPIO.output(4, 0)
  GPIO.output(26, 0)
  GPIO.cleanup()
  print("Cleaned up after catching exception. Now re-throwing.")
  raise
