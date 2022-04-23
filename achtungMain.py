# -*- coding: utf-8 -*-
import pygame
import sys
import achtungGame as game
from settings import SNAKE_COLORS, USE_FULL_SCREEN, USE_GPIO_INPUT, SCREEN_HEIGHT, SCREEN_WIDTH, GAME_FPS
from pygame.locals import *

if USE_GPIO_INPUT:
    import gpioInputModule as inputModule
else:
    import keyboardInputModule as inputModule


pygame.init()
fpsClock = pygame.time.Clock()
readyFont = pygame.font.Font('freesansbold.ttf', 25)
spelaFont = pygame.font.Font('freesansbold.ttf', 50)
logoFont = pygame.font.Font('freesansbold.ttf', 200)

if USE_FULL_SCREEN:
    windowSurfaceObj = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    windowSurfaceObj = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('!achtung!')

allPlayers = game.allPlayers

def activePlayers():
    p = []
    for player in allPlayers:
        if player.ready:
            p.append(player)
    return p

def playersReady():
    yeah = 0
    for player in allPlayers:
        if player.ready:
            yeah+=1
    return yeah

def gameCost():
    return playersReady()*3

def displayReadyText(playerId):
    centerx = 0
    centery = 0
    marginh = 20
    if player.playerId < 4: 
        centerx = (3 + player.playerId * 4) * SCREEN_WIDTH / 18
        centery = SCREEN_HEIGHT - marginh
    else:
        centerx = (3 + (player.playerId - 4) * 4) * SCREEN_WIDTH / 18
        centery = marginh
    displayRotatedText('Redo!', readyFont, SNAKE_COLORS[playerId], 0, (centerx, centery))

def displayRotatedText(text, font, color, rot, center):
    readyTextObj = font.render(text, False, color)
    rotatedSurf = pygame.transform.rotate(readyTextObj, rot)
    rotatedRect = rotatedSurf.get_rect()
    rotatedRect.center = center # (centerx,centery)
    windowSurfaceObj.blit(rotatedSurf, rotatedRect)

def displayInfo():
    #creditText = "Riksdaler: " + str(credits)
    creditText = u"Spelet är gratis!"
    displayRotatedText(creditText, readyFont, pygame.Color(0, 255, 255), 0, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    if playersReady()>=2:
        #displayRotatedText('spel: '+str(gameCost())+' Riksdaler',readyFont,pygame.Color(0,255,0),0,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2+50))
        displayRotatedText(str(playersReady()) + u' spelare är redo!',readyFont,pygame.Color(0,255,0),0,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2+50))

        displayRotatedText(u'Poäng för att vinna: '+str(playersReady()*10-10),readyFont,pygame.Color(120,0,255),0,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2+100))


def displayTextAndLogo():
    displayRotatedText('spela',spelaFont,pygame.Color(255,0,255),45,(SCREEN_WIDTH/4,SCREEN_HEIGHT/4))
    displayRotatedText('ACHTUNG!',spelaFont,pygame.Color(255,50,20),0,(SCREEN_WIDTH/2,SCREEN_HEIGHT/3))


def check_exit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

#collect Money
#credits = 30
#The main loop!!
while True:
    game.resetPlayers()
    #let players ready up
    while True:
        windowSurfaceObj.fill(pygame.Color(0,0,0))
        displayTextAndLogo()
        displayInfo()
        for player in allPlayers:
            if 'l' in inputModule.takeInput(player.playerId): #Maybe use event queue?
                player.ready = True
            elif 'r' in inputModule.takeInput(player.playerId):
                player.ready = False
            if player.ready:
                displayReadyText(player.playerId)

        pressed = pygame.key.get_pressed() # perhaps use the event queue?
        if pressed[K_SPACE]:
            if playersReady()>1:# and gameCost()<=credits:
                #Start the game!
                #credits-=gameCost()
                break #Break here to reach the game loop!

        pygame.display.update()
        fpsClock.tick(GAME_FPS)
        pygame.event.pump() # THIS MUST BE DONE!!!
        check_exit_event()
    # The actual game loop!!
    game.gameLoop(activePlayers(), windowSurfaceObj)
    # Score screen
    # Ad screen
