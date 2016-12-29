import pygame, inputModule,time
from pygame.locals import *
import achtungGame as game

margin = 100


def scoreScreen(players,pygameSurface):
    font = pygame.font.Font('freesansbold.ttf',25)
    pygameSurface.fill(game.backgroundColor)
    i = 0
    players.sort()
    for player in players:
        #display score under each other
        textSurf = font.render("spelare " + str(player.playerId) +": "+ str(player.score),True,game.colors[player.playerId],game.backgroundColor)
        textRect = textSurf.get_rect()
        textRect.center = (game.screenWidth/2,margin+margin*i)
        pygameSurface.blit(textSurf,textRect)
        i+=1
    pygame.display.update()
    time.sleep(5)
    while True:
        if inputModule.takeStartInput():
            return

