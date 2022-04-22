# -*- coding: utf-8 -*-
import pygame
import time
from pygame.locals import *
from settings import FIELD_COLOR, SCREEN_WIDTH, SNAKE_COLORS

margin = 100


def scoreScreen(players, pygameSurface, inputModule):
    font = pygame.font.Font('freesansbold.ttf', 25)
    pygameSurface.fill(FIELD_COLOR)
    i = 0
    players.sort()
    for player in players:
        # display score under each other
        textSurf = font.render("spelare " + str(player.playerId + 1) + ": " + str(
            player.score), True, SNAKE_COLORS[player.playerId], FIELD_COLOR)
        textRect = textSurf.get_rect()
        textRect.center = (SCREEN_WIDTH/2, margin+margin*i)
        pygameSurface.blit(textSurf, textRect)
        i += 1
    pygame.display.update()
    time.sleep(2)
    while True:
        if inputModule.takeStartInput():
            return
