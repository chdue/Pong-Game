import pygame
from pongSupport import *
import random

pygame.init()

screen = pygame.display.set_mode((SCR_W,SCR_H))
pygame.display.set_caption("")
clock = pygame.time.Clock()
done = False

leftPad = Paddle(SCR_W/10,
                 SCR_H/2,
                 PAD_W,
                 PAD_H,
                 WHITE,
                 PAD_SPD,
                 PAD_LEFT)
rightPad = Paddle(SCR_W - SCR_W/10,
                  SCR_H/2,
                  PAD_W,
                  PAD_H,
                  WHITE,
                  PAD_SPD,
                  PAD_RIGHT)
ball = Ball(SCR_W/2,
             SCR_H/2,
             BALL_R,
             WHITE,
             BALL_SPD,
             SPAWN_DEGREE)

uArDown = False
dArDown = False
wDown = False
sDown = False

BALL_LIST = [ball]

while(not done):
    screen.fill(BLACK)

    scoreText = Arial.render("Player 1: %d | %d :Player 2" % (PLScore, PRScore),
                             1, WHITE)
    screen.blit(scoreText, (TEXT_X, TEXT_Y))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                uArDown = True
            elif event.key == pygame.K_DOWN:
                dArDown = True
            elif event.key == pygame.K_w:
                wDown = True
            elif event.key == pygame.K_s:
                sDown = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                uArDown = False
            elif event.key == pygame.K_DOWN:
                dArDown = False
            elif event.key == pygame.K_w:
                wDown = False
            elif event.key == pygame.K_s:
                sDown = False
        
    for i in range(len(BALL_LIST)):   
        BALL_LIST[i].draw(screen)
        BALL_LIST[i].move()
        BALL_LIST[i].checkPaddleCollision(leftPad, COLLISION_LEFT)
        BALL_LIST[i].checkPaddleCollision(rightPad, COLLISION_RIGHT)   
        result = BALL_LIST[i].checkWallCollision(BALL_LIST)
        if (result == SCORE_LEFT):
            PRScore +=1
        elif (result == SCORE_RIGHT):
            PLScore +=1
        if (BALL_LIST[i].Hits == SpawnBallHitNum):
            BALL_LIST.append (Ball(SCR_W/2,
                                   SCR_H/2,
                                   BALL_R,
                                   WHITE,
                                   BALL_SPD,
                                   SPAWN_DEGREE))
            BALL_LIST[i].Hits -= NewBallHitNum
    for i in toRemove:
        BALL_LIST.pop(i)
    toRemove.clear()

    if (uArDown):
        rightPad.moveUp()
        rightPad.checkPaddleWallCollision()
    if (dArDown):
        rightPad.moveDown()
        rightPad.checkPaddleWallCollision()
    if (wDown):
        leftPad.moveUp()
        leftPad.checkPaddleWallCollision()
    if (sDown):
        leftPad.moveDown()
        leftPad.checkPaddleWallCollision()
    
    leftPad.draw(screen)
    rightPad.draw(screen)

    pygame.display.flip()
 
    clock.tick(TIME)

pygame.quit()
