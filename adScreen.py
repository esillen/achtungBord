# -*- coding: utf-8 -*-
import pygame
import time
import drawing
from pygame.locals import *
from settings import BACKGROUND_COLOR, FIELD_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, TIME_UNTIL_AD_SCREEN_TIMEOUT_SECONDS

def adScreen(pygameSurface, inputModule):
    pygameSurface.fill(FIELD_COLOR)
    drawing.drawText("Tyckte du om spelet?", 50, (SCREEN_WIDTH/2, 200), BACKGROUND_COLOR, pygameSurface)
    drawing.drawText("Swisha gärna lite dricks", 50, (SCREEN_WIDTH/2, 300), BACKGROUND_COLOR, pygameSurface)
    pygame.display.update()
    time.sleep(5) # So no-one accidentally keeps the button pressed
    drawing.drawText("Tryck på stora knappen för att fortsätta", 30, (SCREEN_WIDTH/2, SCREEN_HEIGHT - 50), BACKGROUND_COLOR, pygameSurface)
    pygame.display.update()
    start_of_wait_time = time.time()
    while True:
        if time.time() - start_of_wait_time > TIME_UNTIL_AD_SCREEN_TIMEOUT_SECONDS:
            return
        pygame.event.pump()
        if inputModule.takeStartInput():
            return