import sys
import asyncio
import pygame
from random import randrange, uniform, randint

from utils import *
from script.bird import Bird
from script.environment import Environment
from script.ground import Ground

class PyBird():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("PyBird")
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SRCALPHA)
        self._grid_background()

        self.bird_group = pygame.sprite.Group()
        self.bird = Bird(
            groups= self.bird_group,
            position= pygame.Vector2(WIDTH//2, HEIGHT//2),
            anchor= 'center',
            sheet= BIRD_SHEET,
        )

        self.environment_sheet = pygame.sprite.Group()
        for _ in range(5):
            Environment(
                self.environment_sheet,
                pygame.Vector2(randint(16, WIDTH-16), randint(16, HEIGHT-16)),
                anchor='center',
                speed= uniform(10.5, 50),
                frames= BACKGROUND_AIR,
            )
        self.environment_event = pygame.USEREVENT + abs(hash('environment')) % 1000
        pygame.time.set_timer(self.environment_event, 4000)

        self.ground_group = pygame.sprite.Group()
        self.generate_ground(WIDTH//2)
        self.ground_event = pygame.USEREVENT + abs(hash('ground')) % 1000
        self.ground_spawn_timer = 15
        pygame.time.set_timer(self.ground_event, self.ground_spawn_timer* 1000)
        # self.generate_ground(WIDTH)
        # for x in range(0, WIDTH, 48):
        #     self.generate_ground(x)

    def _grid_background(self) -> None:
        self.background = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

        for x in range(0, WIDTH, 16):
            pygame.draw.line(self.background, pygame.Color(173, 170, 170, 75), (x, 0), (x, HEIGHT)) 
        for y in range(0, HEIGHT, 16):
            pygame.draw.line(self.background, pygame.Color(173, 170, 170, 75), (0, y), (WIDTH, y)) 
    
    def render(self) -> None:
        self.screen.fill(BACKGROUND_BLACK)
        self.screen.blit(self.background)

        self.environment_sheet.draw(self.screen)
        # self.bird_group.draw(self.screen)
        # self.bird.render()
        self.ground_group.draw(self.screen)
        
        # for i, tile in enumerate(self.env_sheet.animation_list):
        #     scaled = pygame.transform.scale(tile, (40, 40))
        #     self.screen.blit(scaled, ((i%16)* 40, (i//16)* 40))
        
    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.environment_event:
                self.add_air()
            # if event.type == self.ground_event:
            #     self.generate_ground(WIDTH)
        
    def update(self, deltaTime: float) -> None:
        self.bird_group.update(deltaTime)
        self.environment_sheet.update(deltaTime)
        # self.ground_group.update(deltaTime)
    
    def add_air(self) -> None:
        air = Environment(
            self.environment_sheet,
            pygame.Vector2(WIDTH+16, randint(16, HEIGHT-16)),
            anchor='center',
            speed= uniform(10.5, 50),
            frames= BACKGROUND_AIR,
        )

    def generate_ground(self, coord_x) -> None:
        x = randrange(80, HEIGHT-136, 16)
        y = HEIGHT - 128 - x

        print(x, x//16)
        t = Ground(
            self.ground_group,
            pygame.Vector2(coord_x, x),
            anchor= 'bottomleft',
            height= x//16,
            ground_tiles= GROUND,
            foliage_tiles= FOLIAGE,
            speed= 45.0,
        )
        t.image = pygame.transform.flip(t.image, False, True)
        Ground(
            self.ground_group,
            pygame.Vector2(coord_x, (HEIGHT- y)),
            height= (HEIGHT-x)//16 -8,
            ground_tiles= GROUND,
            foliage_tiles= FOLIAGE,
            speed= 45.0
        )

async def main() -> None:
    deltaTime: float = 0.0
    clock = pygame.time.Clock()
    game = PyBird()
    while True:
        game.render()
        game.handle_input()
        game.update(deltaTime)

        deltaTime = clock.tick(60) / 1000
        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
