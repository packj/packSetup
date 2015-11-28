#!/usr/bin/python

import RPi.GPIO as GPIO
import time

#print GPIO.VERSION

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH)

t=.05

def blink():
    GPIO.output(17, GPIO.LOW)
    time.sleep(t)
    GPIO.output(17, GPIO.HIGH)
    time.sleep(t)

def dot():
    GPIO.output(17, GPIO.LOW)
    time.sleep(.14)
    GPIO.output(17, GPIO.HIGH)
    time.sleep(.3)

def dash():
    GPIO.output(17, GPIO.LOW)
    time.sleep(.35)
    GPIO.output(17, GPIO.HIGH)
    time.sleep(.3)


def M():
    dash()
    dash()
    time.sleep(.4)

def A():
    dot()
    dash()
    time.sleep(.4)

def K():
    dash()
    dot()
    dash()
    time.sleep(.4)

def E():
    dot()
    time.sleep(.4)


def N():
    dash()
    dot()
    time.sleep(.4)


def B():
    dash()
    dot()
    dot()
    dot()
    time.sleep(.4)


def C():
    dash()
    dot()
    dash()
    dot()
    time.sleep(.4)


def D():
    dash()
    dot()
    dot()
    time.sleep(.4)


def F():
    dot()
    dot()
    dash()
    dot()
    time.sleep(.4)


def G():
    dash()
    dash()
    dot()
    time.sleep(.4)


def H():
    dot()
    dot()
    dot()
    dot()
    time.sleep(.4)


def I():
    dot()
    dot()
    time.sleep(.4)


def J():
    dot()
    dash()
    dash()
    dash()
    time.sleep(.4)


def L():
    dash()
    dot()
    dash()
    time.sleep(.4)


def O():
    dash()
    dash()
    dash()
    time.sleep(.4)


def P():
    dot()
    dash()
    dash()
    dot()
    time.sleep(.4)


def Q():
    dash()
    dash()
    dot()
    dash()
    time.sleep(.4)


def R():
    dot()
    dash()
    dot()
    time.sleep(.4)


def S():
    dot()
    dot()
    dot()
    time.sleep(.4)


def T():
    dash()
    time.sleep(.4)


def U():
    dot()
    dot()
    dash()
    time.sleep(.4)


def V():
    dot()
    dot()
    dot()
    dash()
    time.sleep(.4)


def W():
    dot()
    dash()
    dash()
    time.sleep(.4)


def X():
    dash()
    dot()
    dot()
    dash()
    time.sleep(.4)


def Y():
    dash()
    dot()
    dash()
    dash()
    time.sleep(.4)


def Z():
    dash()
    dash()
    dot()
    dot()
    time.sleep(.4)


def N():
    dash()
    dot()
    time.sleep(.4)

#for i in range(120):
#    blink()

Y()
O()
U()

S()
H()
O()
U()
L()
D()

N()
O()
T()

J()
U()
M()
P()

O()
N()

T()
H()
E()

S()
P()
I()
K()
E()
S()


GPIO.cleanup()

