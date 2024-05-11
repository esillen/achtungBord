# -*- coding: utf-8 -*-

import pygame
import sys
import playerModule
import drawing
from pygame.locals import *

from settings import BACKGROUND_COLOR, FIELD_COLOR, INPUT_MODULE, SNAKE_COLORS, SCREEN_HEIGHT, \
    SCREEN_WIDTH, SNAKE_SIZE, BLINK_TIME, SPAWN_TIME, GAME_FPS
if INPUT_MODULE == "GPIO":
    import gpioInputModule as inputModule
elif INPUT_MODULE == "KEYBOARD":
    import keyboardInputModule as inputModule
elif INPUT_MODULE == "JOYSTICK":
    import joystickInputModule as inputModule
else:
    raise Exception("Bad input module")

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

def spawnPlayers(players, pygameSurface):
    spawnedPlayers = []
    for player in players:
        player.resetRandomize(len(players))
        spawnedPlayers.append(player)
        # Take this much time for this player, and additional time for the last player
        delayTime = BLINK_TIME
        if len(spawnedPlayers) == len(players):
            delayTime = BLINK_TIME + 15
        for i in range(delayTime):
            # TODO: add some delay between spawns
            drawing.drawField(len(players), pygameSurface)
            for player in spawnedPlayers:
                player.updateDirection(
                    inputModule.takeInput(player.playerId))
                tempPlayerPos = player.getRoundedPos()
                pygame.draw.circle(
                    pygameSurface, (player.color), tempPlayerPos, SNAKE_SIZE)
                pygame.draw.aaline(pygameSurface, (player.color), tempPlayerPos, (
                    tempPlayerPos[0] + player.currentDirection[0]*directionLineLen, tempPlayerPos[1] + player.currentDirection[1]*directionLineLen), 1)
            pygame.display.update()
            fpsClock.tick(GAME_FPS)
            pygame.event.pump()
            check_exit_event()

def spawnPlayers2(players, pygameSurface):
    for player in players:
        player.resetRandomize(len(players))
    for time_tick in range(SPAWN_TIME * GAME_FPS):
        pygameSurface.fill(BACKGROUND_COLOR)
        drawing.drawField(len(players), pygameSurface)
        
        time_tick_fraction = time_tick / (SPAWN_TIME * GAME_FPS)
        for player in players:
            player.updateDirection(
                inputModule.takeInput(player.playerId))
            tempPlayerPos = player.getRoundedPos()
            drawing.drawSpawnPositionHelperLine(player, time_tick_fraction, pygameSurface)
            pygame.draw.circle(
                pygameSurface, (player.color), tempPlayerPos, SNAKE_SIZE)
            pygame.draw.aaline(pygameSurface, (player.color), tempPlayerPos, (
                tempPlayerPos[0] + player.currentDirection[0]*directionLineLen, tempPlayerPos[1] + player.currentDirection[1]*directionLineLen), 1)
        
        drawing.drawInGameScores(players, pygameSurface)
        pygame.display.update()
        fpsClock.tick(GAME_FPS)
        pygame.event.pump()
        check_exit_event()
    

def updateKurves(players, pygameSurface):
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
                drawing.drawInGameScores(players, pygameSurface)
    pygame.display.update()
    pygame.event.pump()
    fpsClock.tick(GAME_FPS)
    check_exit_event()

# Players is a list of player objects
def gameLoop(players, pygameSurface):
 
    while True:
        # Make a surface in the game field
        pygameSurface.fill(BACKGROUND_COLOR)
        drawing.drawField(len(players), pygameSurface)
        drawing.drawInGameScores(players, pygameSurface)
        pygame.display.update()

        spawnPlayers2(players, pygameSurface)

        pygameSurface.fill(BACKGROUND_COLOR)
        drawing.drawField(len(players), pygameSurface)
        drawing.drawInGameScores(players, pygameSurface)
        
        # So that we don't collide in our line
        for player in players:
            player.updateDirection(inputModule.takeInput(player.playerId))
            tempPlayerPos = player.getRoundedPos()
            pygame.draw.circle(pygameSurface, (player.color),
                               tempPlayerPos, SNAKE_SIZE)

        # gogoog!!!!! :D:D:D:D:D
        while countPlayersStillAlive(players) > 1:
            updateKurves(players, pygameSurface)

        # ONLY ONE SURVIVOR HERE! (ROUND IS OVER)
        alive_color = BACKGROUND_COLOR # Fallback if all dies simultaneously
        for player in players:
            if player.alive:
                alive_color = player.color
                break
        s_pressed_time = 0.0
        drawing.drawText(u"Rundan är över!", 60, (SCREEN_WIDTH / 2,
                 (SCREEN_HEIGHT / 2) - 40), alive_color, pygameSurface)
        drawing.drawText(u"Tryck start: nästa runda", 20, (SCREEN_WIDTH /
                 2, SCREEN_HEIGHT / 2), alive_color, pygameSurface)
        drawing.drawText(u"Håll start: huvudmenyn", 20, (SCREEN_WIDTH / 2,
                 SCREEN_HEIGHT / 2 + 20), alive_color, pygameSurface)
        while True:
            if inputModule.takeStartInput():
                s_pressed_time += 1.0/30.0
                if s_pressed_time > 0.5:
                    pygame.draw.circle(
                        pygameSurface, BACKGROUND_COLOR, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100), 40)
                    pygame.draw.circle(
                        pygameSurface, FIELD_COLOR, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100), 39)
                    pygame.draw.circle(pygameSurface, BACKGROUND_COLOR, (
                        SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100), int(39.9*(s_pressed_time/5.0)))
            elif s_pressed_time > 0.001:
                break
            if s_pressed_time > 5.0:
                return
            # fancy artsy stuff happen here
            pygame.display.update()
            pygame.event.pump()
            fpsClock.tick(GAME_FPS)
            check_exit_event()
        for player in players:
            if player.score >= len(players) * 10 - 10: # Victory condition satisfied
                return


def countPlayersStillAlive(players):
    alive = 0
    for player in players:
        if player.alive:
            alive += 1
    return alive


def updateScores(players):
    for player in players:
        if player.alive:
            player.score += 1  # Update score here


