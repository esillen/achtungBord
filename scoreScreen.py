# -*- coding: utf-8 -*-
import pygame
import time
import drawing
from pygame.locals import *
from settings import FIELD_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH, SNAKE_COLORS, BACKGROUND_COLOR, TIME_UNTIL_SCORE_SCREEN_TIMEOUT_SECONDS

margin = 125


def scoreScreen(players, pygameSurface, inputModule):
    pygameSurface.fill(FIELD_COLOR)
    players.sort()
    for (position, player) in enumerate(players):
        # display score under each other
        if position == 0:
            text = f"BÄST! >>> Spelare {player.playerId + 1}: {player.score} poäng <<<!!!!!!"
        else:
            text = f"Spelare {player.playerId + 1}: {player.score} poäng"
        drawing.drawText(text, 50, (SCREEN_WIDTH/2, margin*(1+position)), SNAKE_COLORS[player.playerId], pygameSurface)
        #textSurf = font.render(text, True, SNAKE_COLORS[player.playerId], FIELD_COLOR)
        #textRect = textSurf.get_rect()
        #textRect.center = (SCREEN_WIDTH/2, margin+margin*i)
        #pygameSurface.blit(textSurf, textRect)
    pygame.display.update()
    time.sleep(2) # So no-one accidentally keeps the button pressed
    drawing.drawText("Tryck på stora knappen för att fortsätta", 30, (SCREEN_WIDTH/2, SCREEN_HEIGHT - 50), BACKGROUND_COLOR, pygameSurface)
    pygame.display.update()
    start_of_wait_time = time.time()
    while True:
        if time.time() - start_of_wait_time > TIME_UNTIL_SCORE_SCREEN_TIMEOUT_SECONDS:
            return
        pygame.event.pump()
        if inputModule.takeStartInput():
            return
