import pygame
from pygame.locals import *
import RPi.GPIO as GPIO

p1 = (2,3)
p2 = (17,27)
p3 = (10,9)
p4 = (5,6)
p5 = (13,19)
p6 = (14,15)
p7 = (23,24)
p8 = (16,20)

playerInputs = (p1,p2,p3,p4,p5,p6,p7,p8)

startInput = 21

def setup_inputs():
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for inputs in playerInputs:
        GPIO.setup(inputs[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(inputs[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)

def takeInput(playerId):
    string = ''
    if not GPIO.input(playerInputs[playerId][0]):
        string+='l'
    if not GPIO.input(playerInputs[playerId][1]):
        string+='r'
    return string

def takeStartInput():
    if not GPIO.input(21):
        return True
    return False
