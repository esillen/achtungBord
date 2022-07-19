# -*- coding: utf-8 -*-
import pygame
import time
from pygame.locals import *
from settings import FIELD_COLOR, SCREEN_WIDTH, SNAKE_COLORS, TIME_UNTIL_SCORE_SCREEN_TIMEOUT_SECONDS

margin = 125


def scoreScreen(players, pygameSurface, inputModule):
    font = pygame.font.Font('freesansbold.ttf', 50)
    pygameSurface.fill(FIELD_COLOR)
    i = 0
    players.sort()
    for (position, player) in enumerate(players):
        # display score under each other
        if position == 0:
            text = f"BÄST! >>> Spelare {player.playerId + 1}: {player.score} poäng <<<!!!!!!"
        else:
            text = f"Spelare {player.playerId + 1}: {player.score} poäng"
        textSurf = font.render(text, True, SNAKE_COLORS[player.playerId], FIELD_COLOR)
        textRect = textSurf.get_rect()
        textRect.center = (SCREEN_WIDTH/2, margin+margin*i)
        pygameSurface.blit(textSurf, textRect)
        i += 1
    pygame.display.update()
    time.sleep(2) # So no-one accidentally keeps the button pressed
    start_of_wait_time = time.time()
    while True:
        if time.time() - start_of_wait_time > TIME_UNTIL_SCORE_SCREEN_TIMEOUT_SECONDS:
            return
        pygame.event.pump()
        if inputModule.takeStartInput():
            return
