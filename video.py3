#!/usr/bin/env python
import time
import datetime
import signal
import sys
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
            'Video_%s.avi' % dateString 
]
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

print("Waiting to finish video...")
pipe.wait()
print("Done.")
