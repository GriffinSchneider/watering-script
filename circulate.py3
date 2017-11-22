#!/usr/bin/env python
import time
import datetime
import signal
import sys
import RPi.GPIO as GPIO
import subprocess as sp

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

def signal_handler(signal, frame):
  print('SIGINT Received')
  GPIO.output(26, 0)
  GPIO.cleanup()
  print('Cleaned up. Exiting.')
  sys.exit(1)
signal.signal(signal.SIGINT, signal_handler)

GPIO.output(26, 0)

print("Waiting...")

time.sleep(1)

print("Circulating...")

GPIO.output(26, 1)
time.sleep(18)
GPIO.output(26, 0)

print("Circulating stopped.")
time.sleep(1)

GPIO.output(26, 0)
GPIO.cleanup()

print("Cleanup complete.")

sp.call(["wall", "Just Circulated"])

print("Done.")
