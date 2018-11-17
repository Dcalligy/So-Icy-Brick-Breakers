import math
import os
import random
import sys
import time
import pygame

"""
TODO
- Create a pause feature
- Create a starting screen
- Make Gucci Mane's face spin when hit'
- Add new paddle?
"""
 
class brickBreaker():

    def main(self):
         
        xSpeed_init = 5
        ySpeed_init = 5
        maxLives = 6
        batSpeed = 30
        score = 0
        bgColour = 255, 0, 23 # Red background 
        size = width, height = 640, 480
 
        pygame.init()
        pygame.display.set_caption('So Icy Brick Breakers')          
        screen = pygame.display.set_mode(size)
        # Fullscreen looks ugly af
        # screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
         
        bat = pygame.image.load("bat.png").convert()
        batRect = bat.get_rect()
 
        ball = pygame.image.load("guwopball.png").convert()
        ball.set_colorkey((255, 255, 255))
        ballRect = ball.get_rect()

        """
        Create a dictionary list with different 
        sounds bits and randomly choose them 
        pong = pygame.mixer.Sound(['Gucci-Burr.wav', 'Lemmuh.wav', ''])
        """
        pong = pygame.mixer.Sound('Gucci-Burr.wav')
        pong.set_volume(10)        
       
        wall = trumpWall()
        wall.buildWall(width)
 
        # Set ready for game loop
        batRect = batRect.move((width / 2) - (batRect.right / 2), height - 20)
        ballRect = ballRect.move(width / 2, height / 2)      
        xSpeed = xSpeed_init
        ySpeed = ySpeed_init
        lives = maxLives
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1,30)      
        pygame.mouse.set_visible(0) # Turn off mouse pointer
        
        while 1:
            
            # FPS
            clock.tick(60)
 
            # Create game controls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
 
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_LEFT:                        
                        batRect = batRect.move(-batSpeed, 0)  
                        if (batRect.left < 0):                          
                            batRect.left = 0    
 
                    if event.key == pygame.K_RIGHT:                    
                        batRect = batRect.move(batSpeed, 0)
                        if (batRect.right > width):                            
                            batRect.right = width
 
            # Check if bat has hit ball    
            if ballRect.bottom >= batRect.top and \
               ballRect.bottom <= batRect.bottom and \
               ballRect.right >= batRect.left and \
               ballRect.left <= batRect.right:
 
                ySpeed = -ySpeed                
                pong.play(0)                
                offset = ballRect.center[0] - batRect.center[0]

                # Offset > 0 means ball has hit the right side of the bat                  
                # the angle of ball varies depending on where ball hits bat              
                if offset > 0:

                    if offset > 30:  
                        xSpeed = 7
                    elif offset > 23:                
                        xSpeed = 6
                    elif offset > 17:
                        xSpeed = 5
 
                else:
 
                    if offset < -30:                            
                        xSpeed = -7
                    elif offset < -23:
                        xSpeed = -6
                    elif offset < -17:
                        xSpeed = -5
 
                     
            # Move bat/ball
            ballRect = ballRect.move(xSpeed, ySpeed)
 
            if ballRect.left < 0 or ballRect.right > width:
                xSpeed = -xSpeed
                #random.choice(pong).play(0)                
                pong.play(0)
 
            if ballRect.top < 0:
                ySpeed = -ySpeed      
                pong.play(0)  
                       
            # Check if ball has gone past bat - lose a life
            if ballRect.top > height:
               
                lives -= 1
               
                # Start a new ball
                xSpeed = xSpeed_init
                rand = random.random()                
               
                if random.random() > 0.5:
                    xSpeed = -xSpeed
               
                ySpeed = ySpeed_init            
                ballRect.center = width * random.random(), height / 3                                
               
                if lives == 0:                    
                    msg = pygame.font.Font(None,70).render("Game Over, Pimp", True, (0, 255, 255), bgColour)
                    msgRect = msg.get_rect()
                    msgRect = msgRect.move(width / 2 - (msgRect.center[0]), height / 3)
                    screen.blit(msg, msgRect)
                    pygame.display.flip()
                    """
                        Trigger user key presses
                            - ESC to quit the game
                            - Use any other key to restart the game
                    """

                    while 1:
                        restart = False
                        #pause = False
                        for event in pygame.event.get():
               
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    sys.exit()
                                #if event.key == pygame.K_p:
                                #    state = PAUSE
                                #if event.key == pygame.K_s:
                                #    state = RUNNING
                                #if event.key == pygame.K_c:
                                #   pause = False
                                if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):                                    
                                    restart = True
                                 
                        if restart:                  
                            screen.fill(bgColour)
                            wall.buildWall(width)
                            lives = maxLives
                            score = 0
                            break  

            if xSpeed < 0 and ballRect.left < 0:
                xSpeed = -xSpeed                                
                pong.play(0)
 
            if xSpeed > 0 and ballRect.right > width:
                xSpeed = -xSpeed                              
                pong.play(0)
           
            # Check if ball makes contact with wall
            # If yes then remove a brick and change the direction of the ball
            index = ballRect.collidelist(wall.brickRect)      
            if index != -1:
               
                if ballRect.center[0] > wall.brickRect[index].right or \
                   ballRect.center[0] < wall.brickRect[index].left:
                   xSpeed = -xSpeed
 
                else:
                    ySpeed = -ySpeed                
 
                pong.play(0)              
                wall.brickRect[index:index + 1] = []
                score += 10

            # Displays lives/score             
            screen.fill(bgColour)
            scoreText = pygame.font.Font(None,30).render("Score: " + str(score), True, (0,255,255), bgColour)
            scoretextRect = scoreText.get_rect()
            scoretextRect = scoretextRect.move(width - scoretextRect.right, 0)

            livesText = pygame.font.Font(None, 30).render("Lives: " + str(lives), True, (0, 255, 255), bgColour)
            livestextRect = livesText.get_rect()

            screen.blit(livesText, livestextRect)
            screen.blit(scoreText, scoretextRect)

            for i in range(0, len(wall.brickRect)):
                screen.blit(wall.brick, wall.brickRect[i])    
                        
            # If bricks are gone then rebuild wall
            if wall.brickRect == []:

                # Displays message to user letting them know they won
                winMsg = pygame.font.Font(None,50).render("You Win! Have a SO ICY DAY! BURRR", True, (0, 255, 255), bgColour)
                msgRect = winMsg.get_rect()
                msgRect = msgRect.move(width / 2 - (msgRect.center[0]), height / 3)
                screen.blit(winMsg, msgRect)
                pygame.display.flip()
                time.sleep(3)

                # Reset lives, score and background color
                screen.fill(bgColour)
                lives = maxLives
                score = 0
                
                # Rebuild wall
                wall.buildWall(width)
                xSpeed = xSpeed_init
                ySpeed = ySpeed_init
                ballRect.center = width / 2, height / 2 

            # Display game    
            screen.blit(ball, ballRect)
            screen.blit(bat, batRect)
            pygame.display.flip()
            

class trumpWall():
 
    def __init__(self):
 
        self.brick = pygame.image.load("brick.png").convert()
        brickRect = self.brick.get_rect()
        self.brickLength = brickRect.right - brickRect.left      
        self.brickHeight = brickRect.bottom - brickRect.top            
 
    def buildWall(self, width):        
 
        xPos = 0
        yPos = 60
        adj = 0
        self.brickRect = []
 
        for i in range (0, 52):
                       
            if xPos > width:
                if adj == 0:
                    adj = self.brickLength / 2
                else:
                    adj = 0
 
                xPos = -adj
                yPos += self.brickHeight
               
            self.brickRect.append(self.brick.get_rect())    
            self.brickRect[i] = self.brickRect[i].move(xPos, yPos)
            xPos = xPos + self.brickLength
 
if __name__ == '__main__':
 
    br = brickBreaker()
    br.main()