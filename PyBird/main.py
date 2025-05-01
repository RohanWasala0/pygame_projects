import sys
import asyncio
import pygame
from random import randrange, uniform, randint
from typing import Tuple

from utils import *
from script.bird import Bird
from script.environment import Environment
from script.ground_0 import Ground

class PyBird():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("PyBird")
        print(pygame.get_sdl_version())
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SRCALPHA)
        self._grid_background()
        self.color = pygame.Color('red')

        self.bird_group = pygame.sprite.Group()
        self.bird = Bird(
            groups = self.bird_group,
            idle_animation_list = BIRD_IDLE,
            flap_animation_list = BIRD_FLAP,
            position = pygame.Vector2(WIDTH//2, HEIGHT//2),
            anchor = 'center',
            scale = 4
        )

        self.environment_sheet = pygame.sprite.Group()
        self.environment_event = pygame.USEREVENT + abs(hash('environment')) % 1000
        for _ in range(5):
            temp = Environment(
                self.environment_sheet,
                pygame.Vector2(randint(16, WIDTH-16), randint(16, HEIGHT-16)),
                anchor='center',
                speed= uniform(10.5, 50),
                frames= BACKGROUND_AIR,
            )
        pygame.time.set_timer(self.environment_event, 4000)

        self.ground_group = pygame.sprite.Group()
        self.parallax_group = pygame.sprite.Group()
        self._generate_ground(self.ground_group, WIDTH, scale= 2)
        # self.parallax_background()
        self.ground_event: pygame.Event = pygame.Event(pygame.USEREVENT + abs(hash('ground')) % 1000)
        self.has_spawed = False

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
        self.bird_group.draw(self.screen)
        self.parallax_group.draw(self.screen)
        self.ground_group.draw(self.screen)
        
    def handle_input(self) -> None:
        for event in pygame.event.get():
            # print(dir(event.type))
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.bird.handling_input(event)
            for x in self.environment_sheet.sprites():
                x.handling_input(event)
            if event.type == self.environment_event:
                self.add_air()
            if event.type == self.ground_event.type:
                self._generate_ground(self.ground_group, WIDTH, scale= 2)
                # self.parallax_background()
        
    def update(self, deltaTime: float) -> None:
        # self.has_spawed = False
        self.bird_group.update(deltaTime)
        self.environment_sheet.update(deltaTime)
        self.ground_group.update(deltaTime)


        if self._send_ground_signal():
            if not self.has_spawed:
                pygame.event.post(self.ground_event)
                self.has_spawed = True
        else:
            self.has_spawed = False 
    
    def add_air(self) -> None:
        Environment(
            self.environment_sheet,
            pygame.Vector2(WIDTH+16, randint(16, HEIGHT-16)),
            anchor='center',
            speed= uniform(10.5, 50),
            frames= BACKGROUND_AIR,
        )

    def _generate_ground(
            self,
            ground_group: pygame.sprite.Group,
            x_coordinates: int = 0,
            obstacle_gap: int = 130,
            min_nof_tiles: int = 5,
            tile_size: Tuple[int, int] = (16, 16),
            scale: float = 1.0,
            alpha: int = 255
    ) -> None:
        scaled_tile_width, scaled_tile_height = tuple([x*scale for x in tile_size])

        min_height = min_nof_tiles * scaled_tile_height
        max_height = min_height + obstacle_gap

        x = randrange(int(min_height), int(max_height), int(scaled_tile_height))
        y = HEIGHT - obstacle_gap - x

        top_ground = Ground(
            groups= ground_group,
            position= pygame.Vector2(x_coordinates + (scaled_tile_width*9)//2, 0),
            height_width= (int(x//scaled_tile_height), 9),
            scale= scale,
            ground_tilemap= TILE_SET,
            tile_mask= TILE_MASK,
            _mask= MASKS,
            alpha= alpha,
        )
        top_ground.image = pygame.transform.flip(top_ground.image, False, True)
        top_ground.mask = pygame.mask.from_surface(top_ground.image)
        # top_ground.alpha = alpha
        bottom_ground = Ground(
            groups= ground_group,
            position= pygame.Vector2(x_coordinates + (scaled_tile_width*9)//2, HEIGHT),
            height_width= (int(y//scaled_tile_height), 9),
            scale= scale,
            ground_tilemap= TILE_SET,
            tile_mask= TILE_MASK,
            _mask= MASKS,
            anchor= "bottomleft",
            alpha= alpha,
        )
        # bottom_ground.alpha = alpha

    def _send_ground_signal(
            self,
    ) -> bool:
        last_ground: Ground = self.ground_group.sprites()[-1]
        return int(last_ground.position.x) == WIDTH - (last_ground.image.width//2)
        # print(last_ground.position.x)

    def parallax_background(
            self
    ) -> None:
        # for x in range(3):
        self._generate_ground(self.parallax_group, x_coordinates= 0, scale= 1.6, alpha= 100)
    
    def masked_colision_check(
            self
    ) -> bool:
        return pygame.sprite.spritecollide(self.bird, self.ground_group, False, pygame.sprite.collide_mask)

    def print_text(self):
        print("its working properly")

async def main() -> None:
    deltaTime: float = 0.0
    clock = pygame.time.Clock()
    game = PyBird()
    while True:
        game.render()
        game.handle_input()
        game.update(deltaTime)

        deltaTime = clock.tick(120) / 1000
        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
