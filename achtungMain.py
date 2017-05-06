# -*- coding: utf-8 -*-
import pygame,sys,time
import achtungGame as game
import inputModule,playerModule
from pygame.locals import *

# TODO: implement better collision detection (for instance extra points on the side of le schnake)
# TODO: right now remove coin thingy completely
# TODO: Implement coin thingy in a good way


pygame.init()
fpsClock = pygame.time.Clock()
readyFont = pygame.font.Font('freesansbold.ttf', 25)
spelaFont = pygame.font.Font('freesansbold.ttf', 50)
logoFont = pygame.font.Font('freesansbold.ttf', 200)

windowSurfaceObj = pygame.display.set_mode((game.screenWidth, game.screenHeight))
pygame.display.set_caption('!achtung!')

readyTextPositions = ((100, 0), (100, 50), (100, 100), (100, 150), (100, 200), (100, 250), (100, 300), (100, 350))

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
    centerx = game.textAligns[playerId][1][0]+(game.screenWidth/2-game.textAligns[playerId][1][0])*0.2
    centery = game.textAligns[playerId][1][1]+(game.screenWidth/2-game.textAligns[playerId][1][1])*0.2
    displayRotatedText('Redo!', readyFont, game.colors[playerId], game.textAligns[playerId][0], (centerx, centery))

def displayRotatedText(text, font, color, rot, center):
    readyTextObj = font.render(text, False, color)
    rotatedSurf = pygame.transform.rotate(readyTextObj, rot)
    rotatedRect = rotatedSurf.get_rect()
    rotatedRect.center = center # (centerx,centery)
    windowSurfaceObj.blit(rotatedSurf, rotatedRect)

def displayInfo():
    #creditText = "Riksdaler: " + str(credits)
    creditText = u"Spelet är gratis!"
    displayRotatedText(creditText, readyFont, pygame.Color(0, 255, 255), 0, (game.screenWidth/2, game.screenHeight/2))
    if playersReady()>=2:
        #displayRotatedText('spel: '+str(gameCost())+' Riksdaler',readyFont,pygame.Color(0,255,0),0,(game.screenWidth/2,game.screenHeight/2+50))
        displayRotatedText(str(playersReady()) + u' spelare är redo!',readyFont,pygame.Color(0,255,0),0,(game.screenWidth/2,game.screenHeight/2+50))

        displayRotatedText(u'Poäng för att vinna: '+str(playersReady()*10-10),readyFont,pygame.Color(120,0,255),0,(game.screenWidth/2,game.screenHeight/2+100))


def displayTextAndLogo():
    displayRotatedText('spela',spelaFont,pygame.Color(255,0,255),45,(game.screenWidth/4,game.screenHeight/4))
    displayRotatedText('ACHTUNG!',spelaFont,pygame.Color(255,50,20),0,(game.screenWidth/2,game.screenHeight/3))

#collect Money
#credits = 30
#The main loop!!
exiting = False
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
        if pressed[K_ESCAPE]:
            exiting = True
            break
        if pressed[K_SPACE]:
            if playersReady()>1:# and gameCost()<=credits:
                #Start the game!
                #credits-=gameCost()
                break #Break here to reach the game loop!

        pygame.display.update()
        fpsClock.tick(30)
        pygame.event.pump() # THIS MUST BE DONE!!!
    # The actual game loop!!
    if exiting:
        break
    game.gameLoop(activePlayers(), windowSurfaceObj)
    # Score screen
    # Ad screen
