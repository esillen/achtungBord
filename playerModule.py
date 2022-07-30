# -*- coding: utf-8 -*-
import math
import random
import achtungGame as game
from settings import ANGLE_SPEED, FIELD_COLOR, MIN_HOLE_SIZE, MAX_HOLE_SIZE, FORWARD_SPEED, HOLE_TIMER_MAX, \
    HOLE_TIMER_MIN, PLAY_FIELD_RADIUS, SNAKE_SIZE, SPAWN_MARGIN, SCREEN_HEIGHT, SCREEN_WIDTH, \
    FIELD_HEIGHT_MARGINS, FIELD_WIDTH_MARGINS
# TODO: will this give the same spawn points all the time?


class Player:
    def __init__(self, color, playerId):
        self.ready = False
        self.playerId = playerId
        self.color = color
        self.pos = [0.0, 0.0]
        self.currentAngle = 0.0
        self.currentDirection = (1.0, 0.0)
        self.alive = True
        self.makingHole = False
        self.nextHole = 0
        self.holeTimer = 0
        self.score = 0
        self.holeSize = 0

    # Wtf
    def __lt__(self, other):
        return self.score > other.score

    def updateDirection(self, direction):
        if 'l' in direction:
            self.currentAngle -= ANGLE_SPEED
        if 'r' in direction:
            self.currentAngle += ANGLE_SPEED
        self.currentDirection = (math.cos(math.radians(
            self.currentAngle)), math.sin(math.radians(self.currentAngle)))

    def updatePos(self):
        self.holeTimer += 1
        if self.makingHole == False and self.holeTimer > self.nextHole:
            self.makingHole = True
            self.holeTimer = 0
            self.holeSize = random.randint(MIN_HOLE_SIZE, MAX_HOLE_SIZE)
        elif self.makingHole and self.holeTimer > self.holeSize:
            self.resetHoleTimer()
        # TODO: perhaps return a bunch of positions to make a smooth line? or perhaps pygame.draw.arc!
        self.pos[0] = self.pos[0]+FORWARD_SPEED*self.currentDirection[0]
        self.pos[1] = self.pos[1]+FORWARD_SPEED*self.currentDirection[1]

    def resetHoleTimer(self):
        self.makingHole = False
        self.holeTimer = 0
        self.nextHole = random.randint(HOLE_TIMER_MIN, HOLE_TIMER_MAX)

    def resetRandomize(self, num_players):
        self.resetHoleTimer()
        radii = random.uniform(0, PLAY_FIELD_RADIUS-SPAWN_MARGIN)
        angle = random.uniform(0, 2*math.pi)
        self.currentAngle = math.degrees(random.uniform(0, 2*math.pi))
        self.currentDirection = (math.cos(angle), math.sin(angle))
        hmargin = FIELD_HEIGHT_MARGINS[num_players - 1]
        wmargin = FIELD_WIDTH_MARGINS[num_players - 1]
        x = random.uniform(wmargin * 1.1 + 70, SCREEN_WIDTH - wmargin * 1.1 - 70)
        y = random.uniform(hmargin * 1.1 + 70, SCREEN_HEIGHT - hmargin * 1.1 - 70)
        self.pos = [x, y]
        self.alive = True

    def checkCollission(self, surface):
        if FIELD_COLOR != surface.get_at((int((2+SNAKE_SIZE)*self.currentDirection[0]+self.pos[0]), int((2+SNAKE_SIZE)*self.currentDirection[1]+self.pos[1]))):
            self.alive = False

    def getRoundedPos(self):
        return (int(self.pos[0]), int(self.pos[1]))

    def resetScore(self):
        self.score = 0

    def reset(self):
        self.__init__(self.color, self.playerId)
