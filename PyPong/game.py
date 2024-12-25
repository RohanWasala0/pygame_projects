import sys
import pygame

from utils import *
from Script.ball import Ball
from Script.paddle import Paddle

from typing import Tuple, Optional

class PyPong():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PyPong")

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

    # region Ball
        self.ball_group = pygame.sprite.Group()
        self.ball = Ball(
            groups= self.ball_group,
            position= pygame.Vector2(WIDTH//2, HEIGHT//2),
            entity_size= (50, 50),
            color= BALL_GREY,
        )
    # endregion
    
    # region Paddle
        self.paddle_group = pygame.sprite.Group()
        self.player1 = Paddle(
            groups= self.paddle_group,
            position= pygame.Vector2(40, HEIGHT//2),
            entity_size= (40, 150),
            color= PADDLE_BROWN,
            input_keys= (pygame.K_w, pygame.K_s),
        )
    # endregion

    def render(self):
        self.screen.fill(BACKGROUND_BLACK)

        self.ball_group.draw(self.screen)
        self.paddle_group.draw(self.screen)

    def handling_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.ball.handling_input(event)
            self.player1.handling_input(event)

    def update(self):
        deltaTime = self.clock.tick() / 1000.0

        self.ball_group.update(deltaTime)
        self.paddle_group.update(deltaTime)

    def run(self):
        while True:
            self.render()
            self.handling_input()
            self.update()

            pygame.display.update()

if __name__ == "__main__":
    PyPong().run()