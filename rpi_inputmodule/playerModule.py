import math,random
import achtungGame as game
#TODO: will this give the same spawn points all the time?

class Player:
    #TODO: is this really how class variables work?
    def __init__(self,color,playerId):
        self.ready = False
        self.playerId = playerId
        self.color = color
        self.pos = [0.0,0.0]
        self.currentAngle = 0.0
        self.currentDirection = (1.0,0.0)
        self.alive = True
        self.makingHole = False
        self.nextHole = 0
        self.holeTimer = 0
        self.score = 0

    def __lt__(self,other):
        return self.score>other.score
        
    def updateDirection(self,direction):
        if 'l' in direction:
            self.currentAngle -= game.angleSpeed
        if 'r' in direction:
            self.currentAngle += game.angleSpeed
        self.currentDirection = (math.cos(math.radians(self.currentAngle)),math.sin(math.radians(self.currentAngle)))
                                          
    def updatePos(self):
        self.holeTimer+=1
        if self.makingHole == False and self.holeTimer>self.nextHole:
            self.makingHole = True
            self.holeTimer=0
        elif self.makingHole and self.holeTimer>game.holeSize:
            self.resetHoleTimer()
        #TODO: perhaps return a bunch of positions to make a smooth line? or perhaps pygame.draw.arc!
        self.pos[0] = self.pos[0]+game.forwardSpeed*self.currentDirection[0]
        self.pos[1] = self.pos[1]+game.forwardSpeed*self.currentDirection[1]
                                          
    def resetHoleTimer(self):
        self.makingHole = False
        self.holeTimer = 0
        self.nextHole = random.randint(game.holeTimerMin,game.holeTimerMax)
                                          
    def resetRandomize(self):
        self.resetHoleTimer()
        radii = random.uniform(0,game.playFieldRadius-game.spawnMargin)
        angle = random.uniform(0,2*math.pi)
        self.currentAngle = math.degrees(random.uniform(0,2*math.pi))
        self.currentDirection = (math.cos(angle),math.sin(angle))
        x = random.uniform(game.wmargin*1.1,game.screenWidth-game.wmargin*1.1)
        y = random.uniform(game.hmargin*1.1,game.screenHeight-game.hmargin*1.1)
        self.pos = [x,y]
        self.alive = True
                                          
    def checkCollission(self,surface):
        if game.fieldColor != surface.get_at((int((2+game.snakeSize)*self.currentDirection[0]+self.pos[0]),int((2+game.snakeSize)*self.currentDirection[1]+self.pos[1]))):
            self.alive = False
                                          
    def getRoundedPos(self):
        return (int(self.pos[0]),int(self.pos[1]))

    def resetScore(self):
        self.score = 0

    def reset(self):
        self.__init__(self.color,self.playerId)
            
