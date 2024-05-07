# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

p1 = (2, 3)
p2 = (17, 27)
p3 = (10, 9)
p4 = (5, 6)
p5 = (13, 19)
p6 = (14, 15)
p7 = (23, 24)
p8 = (16, 20)

playerInputs = (p1, p2, p3, p4, p5, p6, p7, p8)

START_INPUT = 21

def _setup_inputs():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(START_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for inputs in playerInputs:
        GPIO.setup(inputs[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(inputs[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)

def update_pressed():
    pass # Not necessary

def takeInput(playerId):
    string = ''
    if not GPIO.input(playerInputs[playerId][0]):
        string += 'l'
    if not GPIO.input(playerInputs[playerId][1]):
        string += 'r'
    return string


def takeStartInput():
    if not GPIO.input(START_INPUT):
        return True
    return False


_setup_inputs()