import sys
import pygame

from Script.Menu import Menu
from Script.Paddle import Paddle
from Script.ball import Ball

BLACK = (0,0,0)
GREY = (100, 100, 100)
WIDTH, HEIGHT = 640, 480

class Pong:

    def __init__(self, Screen_DIMENSIONS: list) -> None:
        pygame.init()
        pygame.display.set_caption("Game")
        self.font20 = pygame.font.Font('SixtyfourConvergence-Regular-VariableFont_BLED,SCAN,XELA,YELA.ttf', 20)

        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.fps = pygame.time.Clock()
        self.player1_score, self.player2_score = 0, 0

        self.player_1 = Paddle('player', (40, 240), (255, 0, 0), [pygame.K_w, pygame.K_s])
        self.player_2 = Paddle('player', (600, 240), (255, 0, 255), [pygame.K_UP, pygame.K_DOWN])
        self.ball = Ball('ball', (320, 240), (0, 0, 255))
        self.menu = Menu('menu', (0,0), (*GREY, 128))
    
    def textComp(self, displayText: str, textColor: tuple, textPosition: list = [0,0]):
        text = self.font20.render(displayText, True, textColor)
        textrect = text.get_rect()
        textrect.center = textPosition
        self.screen.blit(text, textrect)
        
    def run(self, GAME_FPS: int):
        while True:
            #Render
            self.screen.fill((233, 255, 31))
            
            self.player_1.render(self.screen)
            self.player_2.render(self.screen)
            self.ball.render(self.screen)
            self.menu.render(self.screen, (WIDTH - 50, HEIGHT - 50))
            
            pygame.draw.line(self.screen, BLACK, (WIDTH/2, 0), (WIDTH/2, HEIGHT))
            pygame.draw.line(self.screen, BLACK, (0, HEIGHT/2), (WIDTH, HEIGHT/2))
            
            self.textComp(f'Player1: {self.player1_score} -- Player2: {self.player2_score}', BLACK, [320, 120])
            
            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.player_1.handle(event)
                self.player_2.handle(event)
                self.ball.handle(event)
            
            #game conditions
            # bounce in random direction after hitting a paddle
            if self.ball.X_coordinate >= self.player_1.X_coordinate or self.ball.X_coordinate < self.player_2.X_coordinate:
                if self.player_2.collision_box.colliderect(self.ball.collision_box):
                    self.ball.velocity[0] *= -1
                    self.ball.change_angle([90, 270])
                elif self.player_1.collision_box.colliderect(self.ball.collision_box):
                    self.ball.velocity[0] *= -1
                    self.ball.change_angle([270, 450])
            
            #score counting logic
            if self.ball.X_coordinate <= 0:
                self.ball.velocity = [0,0]
                self.ball.X_coordinate, self.ball.Y_coordinate = 320, 240
                self.player2_score += 1
            elif self.ball.X_coordinate >= 640:
                self.ball.velocity = [0,0]
                self.ball.X_coordinate, self.ball.Y_coordinate = 320, 240
                self.player1_score += 1
                
            #Update 
            self.player_1.update()
            self.player_2.update()
            self.ball.update()
                
            pygame.display.update()
            self.fps.tick(GAME_FPS)
            
            
            
Pong(Screen_DIMENSIONS=(640, 480)).run(GAME_FPS=60)