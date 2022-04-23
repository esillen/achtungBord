# -*- coding: utf-8 -*-
import pygame

# All mentions of "time" without unit mean 1 tick of the clock (nice values for 30 fps)

# General
MAX_NUM_PLAYERS = 4 # Currently only works well with 4 and 8 max players
GAME_FPS = 30

# Input
USE_GPIO_INPUT = False

# Screen
USE_FULL_SCREEN = False
SCREEN_HEIGHT = 540
SCREEN_WIDTH = 960

# Playing field
PLAY_FIELD_RADIUS = (SCREEN_WIDTH // 2) - 20
FIELD_CORNER_RADIUS = 30

# Gameplay settings
ANGLE_SPEED = 5.0
FORWARD_SPEED = 2.5
HOLE_TIMER_MIN = 50
HOLE_TIMER_MAX = 150
SPAWN_MARGIN = 30
SNAKE_SIZE = 3 # Should be an odd number or weird things happen
HOLE_SIZE = 10 # Number of updates during a hole

# Spawn settings
BLINK_TIME = 10
DIRECTION_LINE_LENGTH = SNAKE_SIZE * 3

# Colors
SNAKE_COLORS = (pygame.Color(255, 255, 0), # yellow
                pygame.Color(255, 0, 0), # red
                pygame.Color(0, 255, 0), # green
                pygame.Color(0, 0, 255), # blue
                pygame.Color(255, 255, 255), # white
                pygame.Color(255, 0, 255), # pink
                pygame.Color(0, 255, 255), # teal
                pygame.Color(255, 150, 0)) # orange

BACKGROUND_COLOR = pygame.Color(255, 153, 204) # light pink
FIELD_COLOR = pygame.Color(0, 0, 0) # black

# Misc
TIME_UNTIL_SCORE_SCREEN_TIMEOUT_SECONDS = 15