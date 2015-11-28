#!/usr/bin/python

import RPi.GPIO as GPIO
import time, datetime

def log(m_stri):
    f=open(logfile, 'a')
    now = datetime.datetime.now()
    f.write(now.isoformat() + ' : ' + m_stri + '\n')
    f.close()

def blink():
    print 'SAFETY shutoff!'
    GPIO.output(17, GPIO.LOW)
    time.sleep(10)
    GPIO.output(17, GPIO.HIGH)
    log('safety shutoff')

#print GPIO.VERSION

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

logfile = '/home/pi/code/python/pump/pump.log'

while 1:
    N=0
    while GPIO.input(18)==0:
        time.sleep(.05)
        N+=1
        print N
        if N > 280:
            blink()
    if N > 10:
        log(repr(N))
    time.sleep(.1)

#blink()

GPIO.cleanup()

