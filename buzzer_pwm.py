import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 440)
p.start(0)

for dc in range(0, 101, 5):
    print dc
    p.ChangeDutyCycle(dc)
    time.sleep(1)

raw_input('Press return to stop:')   # use raw_input for Python 2
p.stop()
GPIO.cleanup()
