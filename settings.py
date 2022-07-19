# -*- coding: utf-8 -*-
import pygame

# All mentions of "time" without unit mean 1 tick of the clock (nice values for 30 fps)

# General
MAX_NUM_PLAYERS = 4 # Currently only works well with 4 and 8 max players
GAME_FPS = 30

# Input
USE_GPIO_INPUT = False

# Screen
USE_FULL_SCREEN = True
SCREEN_HEIGHT = 1080 # Don't change this :)
SCREEN_WIDTH = 1920 # Don't change this :)
PHYSICAL_SCREEN_MODE = "TABLE" # "TABLE" or "UPRIGHT". Decides where to draw player texts

# Playing field
PLAY_FIELD_RADIUS = (SCREEN_WIDTH // 2) - 20
FIELD_CORNER_RADIUS = 30
FIELD_HEIGHT_MARGINS = (150, 150, 100, 60, 60, 60, 60, 60) # Margins per number of players
FIELD_WIDTH_MARGINS = (300, 300, 240, 140, 100, 60, 60, 60)

# Gameplay settings
ANGLE_SPEED = 4.5
FORWARD_SPEED = 5.0
HOLE_TIMER_MIN = 40
HOLE_TIMER_MAX = 100
SPAWN_MARGIN = 30
SNAKE_SIZE = 5 # Should be an odd number or weird things happen
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

# Text poses (x, y, angle_degrees)
# Poses are different for table and upright
READY_TEXT_UPRIGHT_POSES = ((384, 900, 0),
                            (768, 900, 0),
                            (1152, 900, 0),
                            (1536, 900, 0),
                            (384, 120, 0),
                            (768, 120, 0),
                            (1152, 120, 0),
                            (1536, 120, 0))
READY_TEXT_TABLE_POSES = ((960, 960, 0),
                          (1800, 940, 45),
                          (1820, 540, 90),
                          (1800, 120, 135),
                          (960, 100, 180),
                          (120, 120, 225),
                          (100, 540, 270),
                          (120, 940, 315))

SCORE_TEXT_UPRIGHT_POSES = ((384, 1050, 0),
                            (768, 1050, 0),
                            (1152, 1050, 0),
                            (1536, 1050, 0),
                            (384, 30, 0),
                            (768, 30, 0),
                            (1152, 30, 0),
                            (1536, 30, 0))
SCORE_TEXT_TABLE_POSES = ((960, 1050, 0),
                          (1890, 1050, 45),
                          (1890, 540, 90),
                          (1890, 30, 135),
                          (960, 30, 180),
                          (30, 30, 225),
                          (30, 540, 270),
                          (30, 1050, 315))

# Misc
TIME_UNTIL_SCORE_SCREEN_TIMEOUT_SECONDS = 15