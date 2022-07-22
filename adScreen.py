# -*- coding: utf-8 -*-
import pygame
import time
import drawing
from pygame.locals import *
from settings import BACKGROUND_COLOR, FIELD_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, TIME_UNTIL_AD_SCREEN_TIMEOUT_SECONDS

def adScreen(pygameSurface, inputModule):
    pygameSurface.fill(FIELD_COLOR)
    drawing.drawText("Tyckte du om Achtungbordet?", 50, (SCREEN_WIDTH/2, 100), BACKGROUND_COLOR, pygameSurface)
    drawing.drawText("Swisha gärna lite dricks", 50, (SCREEN_WIDTH/2, 200), BACKGROUND_COLOR, pygameSurface)
    drawing.drawImage('./images/swish.png', (SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 200), (500, 490), pygameSurface)
    drawing.drawImage('./images/build1.png', (SCREEN_WIDTH / 2 - 200 - 650, SCREEN_HEIGHT / 2 - 150), (500, 375), pygameSurface)
    drawing.drawText("Under huven på Achtungbordet", 15, (SCREEN_WIDTH / 2 - 200 - 420, SCREEN_HEIGHT / 2 + 250), BACKGROUND_COLOR, pygameSurface)
    drawing.drawImage('./images/build2.png', (SCREEN_WIDTH / 2 - 200 + 550, SCREEN_HEIGHT / 2 - 150), (500, 375), pygameSurface)
    drawing.drawText("Debugging!", 15, (SCREEN_WIDTH / 2 - 200 + 800, SCREEN_HEIGHT / 2 + 250), BACKGROUND_COLOR, pygameSurface)
    drawing.drawText("...så kan jag fortsätta bygga coola saker för Rosenhill!", 50, (SCREEN_WIDTH/2, SCREEN_HEIGHT - 150), BACKGROUND_COLOR, pygameSurface)
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

if __name__ == "__main__":
  pygame.init() # To initialize fonts etc.

  surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
  import keyboardInputModule as inputModule
  while True:
    adScreen(surface, inputModule)