import sys
import pygame
import random
import pygame_gui

from utils import *
from Script.ball import Ball
from Script.paddle import Paddle
from Script.text_canvas import text_canvas

class PyPong():
    def __init__(self) -> None:
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
        self.player2= Paddle(
            groups= self.paddle_group,
            position= pygame.Vector2(WIDTH-40, HEIGHT//2),
            entity_size= (40, 150),
            color= PADDLE_BROWN,
            input_keys= (pygame.K_UP, pygame.K_DOWN),
        )
    # endregion

    # region Text Canvas
        self.text_canvas_group = pygame.sprite.Group()
        self.testing = text_canvas(
            groups= self.text_canvas_group,
            position= pygame.Vector2(WIDTH//2 , HEIGHT//2),
            font_path= FONT_PATH,
            color= pygame.Color('white'),
            text= f"testing for changes"
        )
        self.test = text_canvas(
            groups= self.text_canvas_group,
            position= pygame.Vector2(80, (40*8)+20),
            font_path= FONT_PATH,
            color= pygame.Color('white'),
            text= f"testing for changes"
        )
    # endregion

    def render(self) -> None:
        self.screen.fill(BACKGROUND_BLACK)
        for x in range(WIDTH):
            pygame.draw.line(self.screen, pygame.Color(173, 170, 170, 10), (x, 0), (x, HEIGHT)) if x%40 == 0 else None
        for y in range(HEIGHT):
            pygame.draw.line(self.screen, pygame.Color(173, 170, 170, 10), (0, y), (WIDTH, y)) if y%40 == 0 else None

        self.ball_group.draw(self.screen)
        self.paddle_group.draw(self.screen)
        self.text_canvas_group.draw(self.screen)

    def handling_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.ball.handling_input(event)
            self.player1.handling_input(event)
            self.player2.handling_input(event)

    def update(self) -> None:
        deltaTime = self.clock.tick() / 1000.0

        self.paddle_collision()

        self.testing.sinusoidal_motion(deltaTime, 9, 0.18, 25)

        self.ball_group.update(deltaTime)
        self.paddle_group.update(deltaTime)
        self.text_canvas_group.update(deltaTime)

    def run(self) -> None:
        while True:
            self.render()
            self.handling_input()
            self.update()

            pygame.display.update()

    def paddle_collision(self) -> None:

        def handle_collision(paddle, direction, angle_range):
            angles = [angle + random.randint(-10, 10) for angle in angle_range]
            randius_offset = direction * self.ball.radius

            self.ball.velocity = self.ball.change_angle(angles)

        if self.player1.rect.colliderect(self.ball.rect):
            handle_collision(self.player1, -1, [315, 405])
        elif self.player2.rect.colliderect(self.ball.rect):
            handle_collision(self.player2, 1, [135, 225])

if __name__ == "__main__":
    PyPong().run()