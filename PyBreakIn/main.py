import sys
import asyncio
from functools import wraps
import pygame
from pygame import Vector2
from typing import List
from random import choice

from utils import *
from scripts.paddle import Paddle
from scripts.ball import Ball
from scripts.brick import Bricks
from input_manager import InputManager

# decorators
def debug(
    grid_color: pygame.Color = pygame.Color(173, 170, 170, 75),
    spacing: int = 40
):
    def decorator(render):
        @wraps(render)
        def wrapper(self, *args, **kwargs):
            grid_surface: pygame.Surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
            
            for x in range(0, WIDTH, spacing):
                pygame.draw.line(grid_surface, grid_color, (x, 0), (x, HEIGHT)) 
            for y in range(0, HEIGHT, spacing):
                pygame.draw.line(grid_surface, grid_color, (0, y), (WIDTH, y)) 

            kwargs['debug_surface'] = grid_surface
            return render(self, *args, **kwargs)
            # return result
        return wrapper
    return decorator

class PyBreakIn():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("PyBreakIn")
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SRCALPHA)
        self.screen_group = pygame.sprite.Group()
        self.screen_input = InputManager()
        self.screen_input.input_chart = {
            'discrete':{
                pygame.QUIT: self.quit,
            }
        }

        self.score = 0

        self.font = pygame.font.Font(None, 36)
        self.brick_group = pygame.sprite.Group()
        self._init_gameObjects()

    def _init_gameObjects(
        self
    ) -> None: 
        self.paddle = Paddle(
            groups= self.screen_group,
            position= Vector2(WIDTH//2, HEIGHT - 128),
            dimensions= (128, 32),
            color= color_palette[2],
            anchor= 'center'
        )
        self.ball = Ball(
            groups= self.screen_group,
            position= Vector2(WIDTH//2, HEIGHT//2),
            dimensions= (32, 32),
            color= color_palette[1],
            anchor= 'center'
        )
        self.layout_bricks([
            [1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1, 1, 1, 1]])

    @debug(spacing= 16)
    def render(
        self,
        debug_surface:pygame.Surface = None,
    ) -> None:
        self.screen.fill(color_palette[4])
        self.screen.blit(debug_surface, (0, 0)) if debug_surface else None

        for index, color in enumerate(color_palette):
            pygame.draw.rect(
                self.screen,
                color,
                pygame.Rect((index*50, 0), (50, 50)),
                
            )
        self.screen_group.draw(self.screen)
        self.ball.draw_trail(self.screen) if len(self.ball.trail) > 0 else None
        self.ball.velocity_vector(self.screen)
        self.brick_group.draw(self.screen)

    def handle_input(self) -> None:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        self.screen_input.handle_input(events, keys)
        self.ball.input_manager.handle_input(events, keys)
        self.paddle.input_manager.handle_input(events, keys)

    def update(self, deltaTime: float) -> None:
        self.screen_group.update(deltaTime)
        self.ball.reflect_on_collision(self.paddle)
        for brick in self.brick_group.sprites():
            if pygame.sprite.collide_mask(self.ball, brick):
                self.ball.velocity = self.ball.rand_velocity()
                self.score += 1
                brick.kill()

        text = f"Score: {self.score}"
        self.screen.blit(self.font.render(text, True, Color('black')), (0, 55))


    def layout_bricks(self, layout: List[List]) -> None:
        brick_size = Vector2(64, 16)
        starting_position = Vector2(96, 96)

        for i, row in enumerate(layout):
            for j, cell in enumerate(row):
                if cell:
                    Bricks(
                        self.brick_group,
                        color= choice(color_palette[4:7]),
                        position= starting_position + Vector2(j*brick_size.x, i*brick_size.y),
                        dimensions= tuple(brick_size)
                    )
            starting_position.x = starting_position.x - 32 if i%2 == 0 else starting_position.x + 32

    def quit(self):
        print("Shuting down")
        pygame.quit()
        sys.exit()

async def main() -> None:
    deltaTime: float = 0.0
    clock = pygame.time.Clock()
    game = PyBreakIn()
    while True:
        game.render()
        game.handle_input()
        game.update(deltaTime)

        deltaTime = clock.tick(120) / 1000
        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())