# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

class JoystickInputConfig:
  def __init__(self, joystick, left_button_id, right_button_id):
    self.joystick = joystick
    self.left_button_id = left_button_id
    self.right_button_id = right_button_id
  
  def left_is_pressed(self):
    return self.joystick.get_button(self.left_button_id)

  def right_is_pressed(self):
    return self.joystick.get_button(self.right_button_id)


pygame.init()
pygame.joystick.init()
joystick0 = pygame.joystick.Joystick(0)
joystick0.init()

joystick1 = pygame.joystick.Joystick(1)
joystick1.init()

p1 = JoystickInputConfig(joystick0, 0, 1)
p2 = JoystickInputConfig(joystick0, 2, 3)
p3 = JoystickInputConfig(joystick0, 4, 5)
p4 = JoystickInputConfig(joystick0, 6, 7)
p5 = JoystickInputConfig(joystick1, 0, 1)
p6 = JoystickInputConfig(joystick1, 1, 2)
p7 = JoystickInputConfig(joystick1, 3, 4)
p8 = JoystickInputConfig(joystick1, 5, 6)

playerInputs = (p1, p2, p3, p4, p5, p6, p7, p8)

start_input_joystick = joystick0
start_input_button = 8

def update():
  pygame.event.get()

def takeInput(playerId):
    string = ''
    if playerInputs[playerId].left_is_pressed():
        string += 'l'
    if playerInputs[playerId].right_is_pressed():
        string += 'r'
    return string


def takeStartInput():
  pygame.event.get()
  if start_input_joystick.get_button(start_input_button):
    return True
  else:
    return False
