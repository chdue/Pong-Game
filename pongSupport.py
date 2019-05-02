import pygame
import math
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 165, 146)
BLUE = (146, 247, 255)
GREEN = (87, 255, 60)
RED = (255, 26, 26)
 
SCR_W = 700
SCR_H = 500

TIME = 60

PAD_W = SCR_W/70
PAD_H = SCR_H/5
PAD_SPD = 5

BALL_R = 8
BALL_SPD = 2
BALL_SPD_INC = 1.2
BALL_MAX_SPD = 12

part = random.randint(1,4)
angle = random.randint(0,50)
SPAWN_DEGREE = part*90 - 70 + angle

SpawnBallHitNum = 4
NewBallHitNum = 2

COLLISION_LEFT = 0
COLLISION_RIGHT = 1

toRemove = []

SCORE_LEFT = -1
SCORE_RIGHT = 1
SCORE_NONE = 0

PLScore = 0
PRScore = 0

PAD_LEFT = 1
PAD_RIGHT = 0

TEXT_SIZE = 20
TEXT_X = 10
TEXT_Y = 10
Arial = pygame.font.SysFont("arial", TEXT_SIZE)

class Paddle():

    def __init__(self, x, y, w, h, col, spd, side):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = col
        self.speed = spd
        self.side = side

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x - self.width/2,
                          self.y - self.height/2,
                          self.width,
                          self.height))
        
        if (self.side == PAD_LEFT):
            pygame.draw.rect(screen, BLACK,
                             (self.x - self.width/2,
                              self.y - self.height/2,
                              self.width * 4/5,
                              self.height * 4/9))
            pygame.draw.rect(screen, BLACK,
                             (self.x - self.width/2,
                              self.y + self.height/18,
                              self.width * 4/5,
                              self.height/2))
        if (self.side == PAD_RIGHT):
            pygame.draw.rect(screen, BLACK,
                             (self.x - (self.width*3/10),
                              self.y - self.height/2,
                              self.width * 4/5,
                              self.height * 4/9))
            pygame.draw.rect(screen, BLACK,
                             (self.x - (self.width*3/10),
                              self.y + self.height/18,
                              self.width * 4/5,
                              self.height/2))
        
        
    def moveUp(self):
        self.y -= self.speed
        
    def moveDown(self):
        self.y += self.speed

    def checkPaddleWallCollision(self):
        if (self.y - self.height/2 <= 0):
            self.y += self.speed
        if (self.y + self.height/2 >= SCR_H):
            self.y -= self.speed
        
class Ball():

    def __init__(self, x, y, r, col, spd, deg):
        self.x = x
        self.y = y
        self.r = r
        self.color = col
        self.speed = spd
        self.degree = deg
        self.xDir = 1
        self.yDir = 1
        self.Hits = 0
        self.offScreen = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (int(round(self.x)), int(round(self.y))),
                           self.r)
        
    def move(self):
        if (self.speed >= BALL_MAX_SPD):
            self.speed = BALL_MAX_SPD
        self.x += (self.xDir *
                    math.cos(math.radians(self.degree)) *
                    self.speed)
        self.y += (self.yDir *
                    math.sin(math.radians(self.degree)) *
                    self.speed)

    def checkWallCollision(self, balls):
        if (self.y + self.r >= SCR_H or self.y - self.r <= 0):
            self.yDir *= -1
            
        if (self.x - self.r >= SCR_W):
            self.offScreen = 1
            for i in range(len(balls)):
                if(all(x.offScreen == 1 for x in balls)):
                    self.reset()
                elif(balls[i].offScreen == 1):
                    toRemove.append(i)
            return SCORE_RIGHT
        
        if (self.x + self.r <= 0):
            self.offScreen = 1
            for i in range(len(balls)):
                if(all(x.offScreen == 1 for x in balls)):
                    self.reset()
                elif(balls[i].offScreen == 1):
                    toRemove.append(i)
            return SCORE_LEFT
        return SCORE_NONE

    def reset(self):
        self.x = SCR_W/2
        self.y = SCR_H/2
        self.offScreen = 0
        self.degree = SPAWN_DEGREE
        self.speed = BALL_SPD
        self.Hits = 0

    def checkPaddleCollision(self, paddle, side):
        bLeft = self.x - self.r
        bRight = self.x + self.r
        pRight = paddle.x + paddle.width/2
        pLeft = paddle.x - paddle.width/2
        pBot = paddle.y - paddle.height/2
        pTop = paddle.y + paddle.height/2
        
        if (side == COLLISION_LEFT):
            if (pLeft <= bLeft <= pRight and pBot <= self.y <= pTop):
                self.x = pRight + self.r
                self.xDir *= -1
                self.speed *= BALL_SPD_INC
                self.Hits += 1
            
        elif (side == COLLISION_RIGHT):
            if (pRight >= bRight >= pLeft and pBot <= self.y <= pTop):
                self.x = pLeft - self.r
                self.xDir *= -1
                self.speed *= BALL_SPD_INC
                self.Hits += 1
