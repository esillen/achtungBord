import pygame
import math
from settings import BACKGROUND_COLOR, FIELD_COLOR, SNAKE_COLORS, SNAKE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, FIELD_CORNER_RADIUS, FIELD_HEIGHT_MARGINS, FIELD_WIDTH_MARGINS, READY_TEXT_UPRIGHT_POSES, READY_TEXT_TABLE_POSES, SCORE_TEXT_UPRIGHT_POSES, SCORE_TEXT_TABLE_POSES, PHYSICAL_SCREEN_MODE

def drawReadyText(playerId, surface):
    color = SNAKE_COLORS[playerId]
    if PHYSICAL_SCREEN_MODE == "UPRIGHT":
        centerx = READY_TEXT_UPRIGHT_POSES[playerId][0]
        centery = READY_TEXT_UPRIGHT_POSES[playerId][1]
        angle = READY_TEXT_UPRIGHT_POSES[playerId][2]
    elif PHYSICAL_SCREEN_MODE == "TABLE":
        centerx = READY_TEXT_TABLE_POSES[playerId][0]
        centery = READY_TEXT_TABLE_POSES[playerId][1]
        angle = READY_TEXT_TABLE_POSES[playerId][2]
    else:
        raise Exception("Oh no! Bad screen mode.")

    drawRotatedText('Redo!', 50, color, angle, (centerx, centery), surface)


def drawField(num_players, surface):
    hmargin = FIELD_HEIGHT_MARGINS[num_players - 1]
    wmargin = FIELD_WIDTH_MARGINS[num_players - 1]

    # Big surface
    pygame.draw.rect(surface, FIELD_COLOR, pygame.Rect(wmargin+FIELD_CORNER_RADIUS, hmargin+FIELD_CORNER_RADIUS,
                     SCREEN_WIDTH-2*wmargin-2*FIELD_CORNER_RADIUS, SCREEN_HEIGHT-2*hmargin-2*FIELD_CORNER_RADIUS))
    # 4 smaller rectangles
    pygame.draw.rect(surface, FIELD_COLOR, pygame.Rect(
        wmargin, hmargin+FIELD_CORNER_RADIUS, FIELD_CORNER_RADIUS, SCREEN_HEIGHT-2*hmargin-2*FIELD_CORNER_RADIUS))
    pygame.draw.rect(surface, FIELD_COLOR, pygame.Rect(wmargin+FIELD_CORNER_RADIUS,
                     hmargin, SCREEN_WIDTH-2*wmargin-2*FIELD_CORNER_RADIUS, FIELD_CORNER_RADIUS))
    pygame.draw.rect(surface, FIELD_COLOR, pygame.Rect(SCREEN_WIDTH-wmargin-FIELD_CORNER_RADIUS,
                     hmargin+FIELD_CORNER_RADIUS, FIELD_CORNER_RADIUS, SCREEN_HEIGHT-2*hmargin-2*FIELD_CORNER_RADIUS))
    pygame.draw.rect(surface, FIELD_COLOR, pygame.Rect(wmargin+FIELD_CORNER_RADIUS, SCREEN_HEIGHT -
                     FIELD_CORNER_RADIUS-hmargin, SCREEN_WIDTH-2*wmargin-2*FIELD_CORNER_RADIUS, FIELD_CORNER_RADIUS))
    # 4 circles in the corners
    pygame.draw.circle(surface, FIELD_COLOR, (wmargin+FIELD_CORNER_RADIUS,
                       hmargin+FIELD_CORNER_RADIUS), FIELD_CORNER_RADIUS)
    pygame.draw.circle(surface, FIELD_COLOR, (SCREEN_WIDTH-wmargin -
                       FIELD_CORNER_RADIUS, hmargin+FIELD_CORNER_RADIUS), FIELD_CORNER_RADIUS)
    pygame.draw.circle(surface, FIELD_COLOR, (wmargin+FIELD_CORNER_RADIUS,
                       SCREEN_HEIGHT-hmargin-FIELD_CORNER_RADIUS), FIELD_CORNER_RADIUS)
    pygame.draw.circle(surface, FIELD_COLOR, (SCREEN_WIDTH-wmargin-FIELD_CORNER_RADIUS,
                       SCREEN_HEIGHT-hmargin-FIELD_CORNER_RADIUS), FIELD_CORNER_RADIUS)


def drawInGameScores(players, surface):
    circle_radius = 25
    for player in players:

        color = SNAKE_COLORS[player.playerId]
        if PHYSICAL_SCREEN_MODE == "UPRIGHT":
            centerx = SCORE_TEXT_UPRIGHT_POSES[player.playerId][0]
            centery = SCORE_TEXT_UPRIGHT_POSES[player.playerId][1]
            angle = SCORE_TEXT_UPRIGHT_POSES[player.playerId][2]
        elif PHYSICAL_SCREEN_MODE == "TABLE":
            centerx = SCORE_TEXT_TABLE_POSES[player.playerId][0]
            centery = SCORE_TEXT_TABLE_POSES[player.playerId][1]
            angle = SCORE_TEXT_TABLE_POSES[player.playerId][2]
        else:
            raise Exception("Oh no! Bad screen mode.")

        pygame.draw.circle(surface, (0, 0, 0), (centerx, centery), circle_radius)
        drawRotatedText(str(player.score), 25, color, angle, (centerx, centery), surface)



def drawText(text, size, pos, color, surface):
    font = pygame.font.Font('freesansbold.ttf', size)
    s_textSurf = font.render(text, True, color, (0, 0, 0))
    textRect = s_textSurf.get_rect()
    textRect.center = (pos[0], pos[1])
    surface.blit(s_textSurf, textRect)

def drawRotatedText(text, size, color, angle, center, surface):
    font = pygame.font.Font('freesansbold.ttf', size)
    readyTextObj = font.render(text, False, color)
    rotatedSurf = pygame.transform.rotate(readyTextObj, angle)
    rotatedRect = rotatedSurf.get_rect()
    rotatedRect.center = center # (centerx,centery)
    surface.blit(rotatedSurf, rotatedRect)

def drawSpawnPositionHelperLine(player, surface):
    color = SNAKE_COLORS[player.playerId]
    if PHYSICAL_SCREEN_MODE == "UPRIGHT":
        centerx = SCORE_TEXT_UPRIGHT_POSES[player.playerId][0]
        centery = SCORE_TEXT_UPRIGHT_POSES[player.playerId][1]
        angle = SCORE_TEXT_UPRIGHT_POSES[player.playerId][2]
    elif PHYSICAL_SCREEN_MODE == "TABLE":
        centerx = SCORE_TEXT_TABLE_POSES[player.playerId][0]
        centery = SCORE_TEXT_TABLE_POSES[player.playerId][1]
        angle = SCORE_TEXT_TABLE_POSES[player.playerId][2]
    else:
        raise Exception("Oh no! Bad screen mode.")

    player_pos = player.getRoundedPos()

    pygame.draw.line(surface, (color), (centerx, centery), player_pos, 1)

def getSpawnArcRect(player):
    player_pos = player.getRoundedPos()
    rect_size = SNAKE_SIZE * 10
    arcrect = pygame.Rect(0, 0, rect_size, rect_size).move(player_pos[0] - (rect_size / 2), player_pos[1] - (rect_size / 2))
    return arcrect

def drawSpawnArc(player, interpolationT, surface):
    color = SNAKE_COLORS[player.playerId]

    #interpolated_x = centerx + (player_pos[0] - centerx) * interpolationT
    #interpolated_y = centery + (player_pos[1] - centery) * interpolationT
    #pygame.draw.line(surface, (color), (centerx, centery), (interpolated_x, interpolated_y), 3)
    #pygame.draw.circle(surface, (color), (centerx, centery), 3)
    #pygame.draw.circle(surface, (color), (interpolated_x, interpolated_y), 3)
    arcrect = getSpawnArcRect(player)
    pygame.draw.arc(surface, (color), arcrect, 0, interpolationT * math.pi * 2, SNAKE_SIZE)
    if interpolationT > 0.05:
        pygame.draw.arc(surface, (color), arcrect, math.pi * 2 * 0.05, interpolationT * math.pi * 2, SNAKE_SIZE)
    if interpolationT > 0.1:
        pygame.draw.arc(surface, (color), arcrect, math.pi * 2 * 0.1, interpolationT * math.pi * 2, SNAKE_SIZE)
