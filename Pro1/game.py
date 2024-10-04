import sys
import pygame

from Script.entities import Entity
from Script.Paddle import Paddle
from Script.ball import Ball

class Template:

    def __init__(self, Screen_DIMENSIONS: list) -> None:
        pygame.init()
        pygame.display.set_caption("Game")

        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.fps = pygame.time.Clock()

        self.player_1 = Paddle('player', (40, 240), [pygame.K_w, pygame.K_s])
        self.player_1.Color = (255, 0, 0)
        self.player_2 = Paddle('player', (600, 240), [pygame.K_UP, pygame.K_DOWN])
        self.player_2.Color = (255, 0, 255)
        self.ball = Ball('ball', (320, 240))
        
    def run(self, GAME_FPS: int):
        while True:
            self.fps.tick(GAME_FPS)
            #Render
            self.screen.fill((233, 255, 31))
            self.player_1.render(self.screen)
            self.player_2.render(self.screen)
            self.ball.render(self.screen)
            pygame.draw.line(self.screen, (0,0,0), (320, 0), (320, 480))
            pygame.draw.line(self.screen, (0,0,0), (0,240), (640, 240))
            
            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.player_1.handle(event)
                self.player_2.handle(event)
                self.ball.handle(event)
            
            #game conditions
            if self.player_2.collision_box.colliderect(self.ball.collision_box):
                self.ball.velocity = [-5, 0]
            elif self.player_1.collision_box.colliderect(self.ball.collision_box):
                self.ball.velocity = [5, 0]
                
            #Update 
            self.player_1.update()
            self.player_2.update()
            self.ball.update()
            
            
            # if self.player_1.collision_box.colliderect(self.collision_area):
            #     #print("collided")
            #     pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            # elif self.player_2.collision_box.colliderect(self.collision_area):
            #     pygame.draw.rect(self.screen, (0, 255, 0), self.collision_area)
            # else:
            #     #print("collided")
            #     pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)
                
            pygame.display.update()
            
            
            
Template(Screen_DIMENSIONS=(640, 480)).run(GAME_FPS=60)