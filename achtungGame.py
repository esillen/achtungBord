# -*- coding: utf-8 -*-

import pygame
import sys
import playerModule
import scoreScreen
from pygame.locals import *

from settings import BACKGROUND_COLOR, FIELD_COLOR, USE_GPIO_INPUT, SNAKE_COLORS, SCREEN_HEIGHT, \
    SCREEN_WIDTH, SNAKE_SIZE, BLINK_TIME
if USE_GPIO_INPUT:
    import gpioInputModule as inputModule
else:
    import keyboardInputModule as inputModule

hmargin = 300
wmargin = 100
fieldCornerRadius = 30
directionLineLen = SNAKE_SIZE*3
holeSize = 10  # Number of updates during a hole

fpsClock = pygame.time.Clock()

allPlayers = []
for i in range(8):
    allPlayers.append(playerModule.Player(SNAKE_COLORS[i], i))


def resetPlayers():
    for p in allPlayers:
        p.reset()

def check_exit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Players is a list of player objects
def gameLoop(players, pygameSurface):
    # Sets up the field size
    global hmargin, wmargin

    if len(players) == 2:
        hmargin = int((1.0/4.0)*SCREEN_HEIGHT)
        wmargin = int((SCREEN_WIDTH-((SCREEN_HEIGHT-2.0*hmargin)))/2.0)
    elif len(players) == 3:
        hmargin = int((1.0/4.0)*SCREEN_HEIGHT)
        wmargin = int((1.0/4.0)*SCREEN_WIDTH)
    elif len(players) == 4:
        hmargin = 50
        wmargin = int((1.0/4.0)*SCREEN_WIDTH)
    elif len(players) == 5:
        hmargin = 50
        wmargin = int((1.0/6.0)*SCREEN_WIDTH)
    elif len(players) == 6:
        hmargin = 50
        wmargin = int((1.0/8.0)*SCREEN_WIDTH)
    else:
        hmargin = 50
        wmargin = 50

    # Start game loop!!

    while True:
        # Make a surface in the game field
        pygameSurface.fill(BACKGROUND_COLOR)
        drawField(pygameSurface)
        drawScores(players, pygameSurface)
        pygame.display.update()
        # spawn players and let them choose their directions
        spawnedPlayers = []
        for player in players:
            player.resetRandomize()
            spawnedPlayers.append(player)
            # Take this much time for this player, and additional time for the last player
            delayTime = BLINK_TIME
            if len(spawnedPlayers) == len(players):
                delayTime = BLINK_TIME + 15
            for i in range(delayTime):
                # TODO: add some delay between spawns
                drawField(pygameSurface)
                for player in spawnedPlayers:
                    player.updateDirection(
                        inputModule.takeInput(player.playerId))
                    tempPlayerPos = player.getRoundedPos()
                    pygame.draw.circle(
                        pygameSurface, (player.color), tempPlayerPos, SNAKE_SIZE)
                    pygame.draw.aaline(pygameSurface, (player.color), tempPlayerPos, (
                        tempPlayerPos[0] + player.currentDirection[0]*directionLineLen, tempPlayerPos[1] + player.currentDirection[1]*directionLineLen), 1)
                pygame.display.update()
                fpsClock.tick(30)
                pygame.event.pump()
                check_exit_event()
        # So that we don't collide in our line
        drawField(pygameSurface)
        for player in players:
            player.updateDirection(inputModule.takeInput(player.playerId))
            tempPlayerPos = player.getRoundedPos()
            pygame.draw.circle(pygameSurface, (player.color),
                               tempPlayerPos, SNAKE_SIZE)
        # wait a little and let the last player choose direction
        # gogoog!!!!! :D:D:D:D:D
        while playersStillAlive(players) > 1:
            # updateKurves
            for player in players:
                if player.alive:
                    player.updateDirection(
                        inputModule.takeInput(player.playerId))
                    player.checkCollission(pygameSurface)
                    # maybe skip this test! (perhaps looks better)
                    if player.alive:
                        if player.makingHole:
                            pygame.draw.circle(pygameSurface, (pygame.Color(
                                0, 0, 0)), player.getRoundedPos(), SNAKE_SIZE)
                        player.updatePos()
                        pygame.draw.circle(
                            pygameSurface, (player.color), player.getRoundedPos(), SNAKE_SIZE)
                    else:
                        updateScores(players)
                        drawScores(players, pygameSurface)
            pygame.display.update()
            pygame.event.pump()
            fpsClock.tick(30)
            check_exit_event()
        # ONLY ONE SURVIVOR HERE! (ROUND IS OVER)
        alive_color = players[0].color # Fallback if all dies simultaneously
        for player in players:
            if player.alive:
                alive_color = player.color
                break
        s_pressed_time = 0.0
        drawText(u"Rundan är över!", 30, (SCREEN_WIDTH / 2,
                 (SCREEN_HEIGHT / 2) - 20), alive_color, pygameSurface)
        drawText(u"Tryck start: nästa runda", 10, (SCREEN_WIDTH /
                 2, SCREEN_HEIGHT / 2), alive_color, pygameSurface)
        drawText(u"Håll start: huvudmenyn", 10, (SCREEN_WIDTH / 2,
                 SCREEN_HEIGHT / 2 + 10), alive_color, pygameSurface)
        while True:
            if inputModule.takeStartInput():
                s_pressed_time += 1.0/30.0
                if s_pressed_time > 0.5:
                    pygame.draw.circle(
                        pygameSurface, BACKGROUND_COLOR, (SCREEN_HEIGHT/2, SCREEN_WIDTH/2 + 50), 20)
                    pygame.draw.circle(
                        pygameSurface, FIELD_COLOR, (SCREEN_HEIGHT/2, SCREEN_WIDTH/2 + 50), 19)
                    pygame.draw.circle(pygameSurface, BACKGROUND_COLOR, (
                        SCREEN_HEIGHT/2, SCREEN_WIDTH/2 + 50), int(19.0*(s_pressed_time/5.0)))
            elif s_pressed_time > 0.001:
                break
            if s_pressed_time > 5.0:
                scoreScreen.scoreScreen(players, pygameSurface, inputModule)
                return
            # fancy artsy stuff happen here
            pygame.display.update()
            pygame.event.pump()
            fpsClock.tick(30)
            check_exit_event()
        for player in players:
            if player.score >= len(players) * 10 - 10:
                scoreScreen.scoreScreen(players, pygameSurface, inputModule)
                return


def drawField(surface):
    # Big surface
    pygame.draw.rect(surface, FIELD_COLOR, pygame.Rect(wmargin+fieldCornerRadius, hmargin+fieldCornerRadius,
                     SCREEN_WIDTH-2*wmargin-2*fieldCornerRadius, SCREEN_HEIGHT-2*hmargin-2*fieldCornerRadius))
    # 4 smaller rectangles
    pygame.draw.rect(surface, FIELD_COLOR, pygame.Rect(
        wmargin, hmargin+fieldCornerRadius, fieldCornerRadius, SCREEN_HEIGHT-2*hmargin-2*fieldCornerRadius))
    pygame.draw.rect(surface, FIELD_COLOR, pygame.Rect(wmargin+fieldCornerRadius,
                     hmargin, SCREEN_WIDTH-2*wmargin-2*fieldCornerRadius, fieldCornerRadius))
    pygame.draw.rect(surface, FIELD_COLOR, pygame.Rect(SCREEN_WIDTH-wmargin-fieldCornerRadius,
                     hmargin+fieldCornerRadius, fieldCornerRadius, SCREEN_HEIGHT-2*hmargin-2*fieldCornerRadius))
    pygame.draw.rect(surface, FIELD_COLOR, pygame.Rect(wmargin+fieldCornerRadius, SCREEN_HEIGHT -
                     fieldCornerRadius-hmargin, SCREEN_WIDTH-2*wmargin-2*fieldCornerRadius, fieldCornerRadius))
    # 4 circles in the corners
    pygame.draw.circle(surface, FIELD_COLOR, (wmargin+fieldCornerRadius,
                       hmargin+fieldCornerRadius), fieldCornerRadius)
    pygame.draw.circle(surface, FIELD_COLOR, (SCREEN_WIDTH-wmargin -
                       fieldCornerRadius, hmargin+fieldCornerRadius), fieldCornerRadius)
    pygame.draw.circle(surface, FIELD_COLOR, (wmargin+fieldCornerRadius,
                       SCREEN_HEIGHT-hmargin-fieldCornerRadius), fieldCornerRadius)
    pygame.draw.circle(surface, FIELD_COLOR, (SCREEN_WIDTH-wmargin-fieldCornerRadius,
                       SCREEN_HEIGHT-hmargin-fieldCornerRadius), fieldCornerRadius)


def playersStillAlive(players):
    alive = 0
    for player in players:
        if player.alive:
            alive += 1
    return alive


def updateScores(players):
    for player in players:
        if player.alive:
            player.score += 1  # Update score here


ptextw = 50
ptexth = 30
textMargin = 50
p1a = (0, (SCREEN_WIDTH/2, SCREEN_HEIGHT-textMargin/2), (ptextw, ptexth))
p2a = (45, (SCREEN_WIDTH-textMargin/2, SCREEN_HEIGHT-textMargin/2), (ptextw, ptexth))
p3a = (90, (SCREEN_WIDTH-textMargin/2, SCREEN_HEIGHT/2), (ptextw, ptexth))
p4a = (135, (SCREEN_WIDTH-textMargin/2, textMargin/2), (ptextw, ptexth))
p5a = (180, (SCREEN_WIDTH/2, textMargin/2), (ptextw, ptexth))
p6a = (225, (textMargin/2, textMargin/2), (ptextw, ptexth))
p7a = (270, (textMargin/2, SCREEN_HEIGHT/2), (ptextw, ptexth))
p8a = (315, (textMargin/2, SCREEN_HEIGHT-textMargin/2), (ptextw, ptexth))

textAligns = (p1a, p2a, p3a, p4a, p5a, p6a, p7a, p8a)


def drawScores(players, surface):
    font = pygame.font.Font('freesansbold.ttf', 30)
    for player in players:

        textSurf = font.render(str(player.score), True,
                               SNAKE_COLORS[player.playerId], (0, 0, 0))
        #rotatedSurf = pygame.transform.scale(textSurf,textAligns[player.playerId][2])
        rotatedSurf = pygame.transform.rotate(
            textSurf, textAligns[player.playerId][0])
        rotatedRect = rotatedSurf.get_rect()
        rotatedRect.center = textAligns[player.playerId][1]
        pygame.draw.circle(surface, (0, 0, 0), (rotatedRect.center), 40)

        surface.blit(rotatedSurf, rotatedRect)


def drawText(text, size, pos, color, surface):
    font = pygame.font.Font('freesansbold.ttf', size)
    s_textSurf = font.render(text, True, color, (0, 0, 0))
    textRect = s_textSurf.get_rect()
    textRect.center = (pos[0], pos[1])
    surface.blit(s_textSurf, textRect)
