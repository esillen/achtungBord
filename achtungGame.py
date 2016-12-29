import pygame,playerModule,inputModule,scoreScreen
from pygame.locals import *
screenHeight = 600
screenWidth = 600
playFieldRadius = screenWidth//2-20
angleSpeed = 5.0
forwardSpeed = 2.5
holeTimerMin = 90
holeTimerMax = 150
spawnMargin = 30
snakeSize = 3
blinkTime = 10
margin = 50
hmargin = 300
wmargin = 100
fieldCornerRadius = 30
directionLineLen = snakeSize*3
holeSize = 10 #Number of updates during a hole
colors = (pygame.Color(255,255,255),pygame.Color(255,0,0),pygame.Color(0,255,0),pygame.Color(0,0,255),pygame.Color(255,255,0),pygame.Color(255,0,255),pygame.Color(0,255,255),pygame.Color(255,150,0))


backgroundColor = pygame.Color(255,153,204) #pink
fieldColor = pygame.Color(0,0,0) #black
fpsClock = pygame.time.Clock()

allPlayers = []
for i in range(8):
    allPlayers.append(playerModule.Player(colors[i],i))

def resetPlayers():
    for p in allPlayers:
        p.reset()


#Players is a list of player objects
def gameLoop(players,pygameSurface):
    #Sets up the field size
    global hmargin,wmargin,margin

    temp = len(players)
    if temp == 2:
        hmargin = int((1.0/4.0)*screenHeight)
        wmargin = int((screenWidth-((screenHeight-2.0*hmargin)))/2.0)
    elif temp == 3:
        hmargin = int((1.0/4.0)*screenHeight)
        wmargin = int((1.0/4.0)*screenWidth)
    elif temp == 4:
        hmargin = 50
        wmargin = int((1.0/4.0)*screenWidth)
    elif temp == 5:
        hmargin = 50
        wmargin = int((1.0/6.0)*screenWidth)
    elif temp == 6:
        hmargin = 50
        wmargin = int((1.0/8.0)*screenWidth)
    else:
        hmargin = 50
        wmargin = 50

    #Start game loop!!
        
    while True:
        #Make a surface in the game field
        pygameSurface.fill(backgroundColor)
        drawField(pygameSurface)
        drawScores(players,pygameSurface)
        pygame.display.update()
        #spawn players and let them choose their directions
        spawnedPlayers = []
        for player in players:
            player.resetRandomize()
            spawnedPlayers.append(player)
            #Take this much time for this player, and additional time for the last player
            delayTime = blinkTime
            if len(spawnedPlayers)==len(players):
                delayTime = blinkTime*5
            for i in range(delayTime):
                #TODO: add some delay between spawns
                drawField(pygameSurface)
                for player in spawnedPlayers:
                    player.updateDirection(inputModule.takeInput(player.playerId))
                    tempPlayerPos = player.getRoundedPos()
                    pygame.draw.circle(pygameSurface,(player.color),tempPlayerPos,snakeSize)
                    pygame.draw.aaline(pygameSurface,(player.color),tempPlayerPos,(tempPlayerPos[0] + player.currentDirection[0]*directionLineLen,tempPlayerPos[1] + player.currentDirection[1]*directionLineLen),1)
                pygame.display.update()
                fpsClock.tick(30)
                pygame.event.pump()
        #So that we don't collide in our line
        drawField(pygameSurface)   
        for player in players:
            player.updateDirection(inputModule.takeInput(player.playerId))
            tempPlayerPos = player.getRoundedPos()
            pygame.draw.circle(pygameSurface,(player.color),tempPlayerPos,snakeSize)
        #wait a little and let the last player choose direction
        #gogoog!!!!! :D:D:D:D:D
        while playersStillAlive(players) > 1:
            #updateKurves
            for player in players:
                if player.alive:
                    player.updateDirection(inputModule.takeInput(player.playerId))
                    player.checkCollission(pygameSurface)
                    if player.alive: #maybe skip this test! (perhaps looks better)
                        if player.makingHole:
                            pygame.draw.circle(pygameSurface,(pygame.Color(0,0,0)),player.getRoundedPos(),snakeSize)
                        player.updatePos()
                        pygame.draw.circle(pygameSurface,(player.color),player.getRoundedPos(),snakeSize)
                    else:
                        updateScores(players)
                        drawScores(players,pygameSurface)
            pygame.display.update()
            pygame.event.pump()
            fpsClock.tick(30)
        ###ONLY ONE SURVIVOR HERE! (ROUND IS OVER)
        alive_color = None
        for player in players:
            if player.alive:
                alive_color = player.color
                break
        s_pressed_time = 0.0
        drawText("Rundan ar over!", 30, (screenWidth/2, screenHeight/2 -20), alive_color, pygameSurface)
        drawText("Tryck start: nasta runda", 10, (screenWidth/2, screenHeight/2 ), alive_color, pygameSurface)
        drawText("Hall start: huvudmenyn", 10, (screenWidth/2, screenHeight/2 + 10), alive_color, pygameSurface)
        while True:
            if inputModule.takeStartInput():
                s_pressed_time += 1.0/30.0
                if s_pressed_time > 0.5:
                    pygame.draw.circle(pygameSurface, backgroundColor, (screenHeight/2, screenWidth/2 + 50), 20)
                    pygame.draw.circle(pygameSurface, fieldColor, (screenHeight/2, screenWidth/2 + 50), 19)
                    pygame.draw.circle(pygameSurface, backgroundColor, (screenHeight/2, screenWidth/2 + 50), int(19.0*(s_pressed_time/5.0)))
            elif s_pressed_time > 0.001:
                break
            if s_pressed_time > 5.0:
                scoreScreen.scoreScreen(players,pygameSurface)
                return
            #fancy artsy stuff happen here
            pygame.display.update()
            pygame.event.pump()
            fpsClock.tick(30)
        for player in players:
            if player.score>=len(players)*10-10:
                scoreScreen.scoreScreen(players,pygameSurface)
                return
        
def drawField(surface):
    #Big surface
    pygame.draw.rect(surface,fieldColor,pygame.Rect(wmargin+fieldCornerRadius,hmargin+fieldCornerRadius,screenWidth-2*wmargin-2*fieldCornerRadius,screenHeight-2*hmargin-2*fieldCornerRadius))
    #4 smaller rectangles
    pygame.draw.rect(surface,fieldColor,pygame.Rect(wmargin,hmargin+fieldCornerRadius,fieldCornerRadius,screenHeight-2*hmargin-2*fieldCornerRadius))
    pygame.draw.rect(surface,fieldColor,pygame.Rect(wmargin+fieldCornerRadius,hmargin,screenWidth-2*wmargin-2*fieldCornerRadius,fieldCornerRadius))
    pygame.draw.rect(surface,fieldColor,pygame.Rect(screenWidth-wmargin-fieldCornerRadius,hmargin+fieldCornerRadius,fieldCornerRadius,screenHeight-2*hmargin-2*fieldCornerRadius))
    pygame.draw.rect(surface,fieldColor,pygame.Rect(wmargin+fieldCornerRadius,screenHeight-fieldCornerRadius-hmargin,screenWidth-2*wmargin-2*fieldCornerRadius,fieldCornerRadius))
    #4 circles in the corners
    pygame.draw.circle(surface,fieldColor,(wmargin+fieldCornerRadius,hmargin+fieldCornerRadius),fieldCornerRadius)
    pygame.draw.circle(surface,fieldColor,(screenWidth-wmargin-fieldCornerRadius,hmargin+fieldCornerRadius),fieldCornerRadius)
    pygame.draw.circle(surface,fieldColor,(wmargin+fieldCornerRadius,screenHeight-hmargin-fieldCornerRadius),fieldCornerRadius)
    pygame.draw.circle(surface,fieldColor,(screenWidth-wmargin-fieldCornerRadius,screenHeight-hmargin-fieldCornerRadius),fieldCornerRadius)
    
def playersStillAlive(players):
    alive = 0
    for player in players:
        if player.alive:
            alive+=1
    return alive

def updateScores(players):
    for player in players:
        if player.alive:
            player.score+=1 #Update score here


ptextw = 50
ptexth = 30
p1a = (0, (screenWidth/2,screenHeight-margin/2),(ptextw,ptexth))
p2a = (45, (screenWidth-margin/2,screenHeight-margin/2),(ptextw,ptexth))
p3a = (90, (screenWidth-margin/2,screenHeight/2),(ptextw,ptexth))
p4a = (135, (screenWidth-margin/2,margin/2),(ptextw,ptexth))
p5a = (180, (screenWidth/2,margin/2),(ptextw,ptexth))
p6a = (225, (margin/2,margin/2),(ptextw,ptexth))
p7a = (270, (margin/2,screenHeight/2),(ptextw,ptexth))
p8a = (315, (margin/2,screenHeight-margin/2),(ptextw,ptexth))

textAligns = (p1a,p2a,p3a,p4a,p5a,p6a,p7a,p8a)


def drawScores(players,surface):
    font = pygame.font.Font('freesansbold.ttf', 30)
    for player in players:

        #textSurf = font.render(str(player.score), True, colors[player.playerId],backgroundColor)
        textSurf = font.render(str(player.score), True, colors[player.playerId],(0,0,0))
        #rotatedSurf = pygame.transform.scale(textSurf,textAligns[player.playerId][2])
        rotatedSurf = pygame.transform.rotate(textSurf, textAligns[player.playerId][0])
        rotatedRect = rotatedSurf.get_rect()
        rotatedRect.center = textAligns[player.playerId][1]
        pygame.draw.circle(surface,(0,0,0),(rotatedRect.center),40)

        surface.blit(rotatedSurf,rotatedRect)


def drawText(text, size, pos, color, surface):
    font = pygame.font.Font('freesansbold.ttf', size)
    s_textSurf = font.render(text, True, color,(0,0,0))
    textRect = s_textSurf.get_rect()
    textRect.center = (pos[0], pos[1])
    surface.blit(s_textSurf,textRect)