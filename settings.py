# -*- coding: utf-8 -*-
import pygame

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
HOLE_TIMER_MIN = 90
HOLE_TIMER_MAX = 150
SPAWN_MARGIN = 30
SNAKE_SIZE = 3
HOLE_SIZE = 10 # Number of updates during a hole

# Spawn settings
BLINK_TIME = 10
DIRECTION_LINE_LENGTH = SNAKE_SIZE * 3

# Colors
SNAKE_COLORS = (pygame.Color(255, 255, 255), pygame.Color(255, 0, 0), pygame.Color(0, 255, 0), pygame.Color(0, 0, 255), pygame.Color(255, 255, 0), pygame.Color(255, 0, 255), pygame.Color(0, 255, 255), pygame.Color(255, 150, 0))
BACKGROUND_COLOR = pygame.Color(255, 153, 204) #pink
FIELD_COLOR = pygame.Color(0, 0, 0) #black