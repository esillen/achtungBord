# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

p1 = (K_a, K_s)
p2 = (K_d, K_f)
p3 = (K_g, K_h)
p4 = (K_j, K_k)
p5 = (K_z, K_x)
p6 = (K_c, K_v)
p7 = (K_b, K_n)
p8 = (K_q, K_w)

playerInputs = (p1, p2, p3, p4, p5, p6, p7, p8)

start_input = K_SPACE


def takeInput(playerId):
    string = ''
    pressed = pygame.key.get_pressed()  # potentially slow to do for each player
    if pressed[playerInputs[playerId][0]]:
        string += 'l'
    if pressed[playerInputs[playerId][1]]:
        string += 'r'
    return string


def takeStartInput():
    pressed = pygame.key.get_pressed()
    if pressed[start_input]:
        return True
    return False
