# -*- coding: utf-8 -*-
import pygame
pygame.init() # To initialize fonts etc.

import sys
import achtungGame as game
import drawing
import scoreScreen
import adScreen
from settings import SNAKE_COLORS, USE_FULL_SCREEN, USE_GPIO_INPUT, SCREEN_HEIGHT, SCREEN_WIDTH, GAME_FPS, DISPLAY_AD_SCREEN
from pygame.locals import *

if USE_GPIO_INPUT:
    import gpioInputModule as inputModule
else:
    import keyboardInputModule as inputModule

pygame.mouse.set_visible(False)

fpsClock = pygame.time.Clock()
infoFont = pygame.font.Font('freesansbold.ttf', 50)
spelaFont = pygame.font.Font('freesansbold.ttf', 100)
logoFont = pygame.font.Font('freesansbold.ttf', 400)

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

def displayInfo():
    #creditText = "Riksdaler: " + str(credits)
    creditText = u"Spelet är gratis!"
    drawing.drawRotatedText(creditText, infoFont, pygame.Color(0, 255, 255), 0, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), windowSurfaceObj)
    if playersReady()>=2:
        #drawing.drawRotatedText('spel: '+str(gameCost())+' Riksdaler',infoFont,pygame.Color(0,255,0),0,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2+50), windowSurfaceObj)
        drawing.drawRotatedText(str(playersReady()) + u' spelare är redo!', infoFont,pygame.Color(0,255,0),0,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2+50), windowSurfaceObj)

        drawing.drawRotatedText(u'Poäng för att vinna: ' + str(playersReady()*10-10), infoFont,pygame.Color(120,0,255), 0, (SCREEN_WIDTH/2,SCREEN_HEIGHT/2+100), windowSurfaceObj)


def displayTextAndLogo():
    drawing.drawRotatedText('spela',spelaFont,pygame.Color(255,0,255),45,(SCREEN_WIDTH/4,SCREEN_HEIGHT/4), windowSurfaceObj)
    drawing.drawRotatedText('ACHTUNG!',spelaFont,pygame.Color(255,50,20),0,(SCREEN_WIDTH/2,SCREEN_HEIGHT/3), windowSurfaceObj)


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
                drawing.drawReadyText(player.playerId, windowSurfaceObj)

        if inputModule.takeStartInput() and playersReady()>1: #and gameCost()<=credits:
            #Start the game!
            #credits-=gameCost()
            break #Break here to reach the game loop!
        

        pygame.display.update()
        fpsClock.tick(GAME_FPS)
        pygame.event.pump() # THIS MUST BE DONE!!!
        check_exit_event()
    players = activePlayers()
    # The actual game loop!!
    game.gameLoop(players, windowSurfaceObj)
    # Score screen
    scoreScreen.scoreScreen(players, windowSurfaceObj, inputModule)
    # Ad screen
    if DISPLAY_AD_SCREEN:
        adScreen.adSreen(windowSurfaceObj, inputModule)
