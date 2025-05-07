import sys
import asyncio
import pygame
from random import randrange, uniform, randint
from typing import Tuple, List
from functools import wraps
from PySignal import Signal

from utils import *
from script.bird import Bird
from script.ground_0 import Ground
from script.text_canvas import text_canvas
from script.environment import Environment

# decorators
def debug(
    grid_color: pygame.Color = Color(173, 170, 170, 75),
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

ground_signal = Signal()
parallax_signal = Signal()

class PyBird():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("PyBird")
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SRCALPHA)

        self._init_gameObjects()
        self.check_index = False 
        self.score = 0
        self.speed = 45
    
    def _init_gameObjects(
        self
    ) -> None: 
        self.bird_group = pygame.sprite.Group()
        self.bird = Bird(
            groups = self.bird_group,
            idle_animation_list = BIRD_IDLE,
            flap_animation_list = BIRD_FLAP,
            position = pygame.Vector2(WIDTH//2 - 16*4, HEIGHT//2),
            anchor = 'center',
            scale = 4
        )
        
        self.environment_group = pygame.sprite.Group()
        self.environment_event = pygame.USEREVENT + abs(hash('environment')) % 1000
        pygame.time.set_timer(self.environment_event, 4000)
        for _ in range(15):
            Environment(
                self.environment_group,
                pygame.Vector2(randint(16, WIDTH-16), randint(16, HEIGHT-16)),
                anchor='center',
                speed= uniform(10.5, 50),
                frames= BACKGROUND_AIR,
            )
        
        self.ground_group = pygame.sprite.Group()
        self.new_generate_ground(
            x_coordinate= WIDTH,
            ground_group= self.ground_group,
            scale= 2.0,
        )
        ground_signal.connect(
            lambda: 
                self.new_generate_ground(
                    x_coordinate= WIDTH,
                    ground_group= self.ground_group,
                    scale= 2.0,
                )
        )
        
        self.canvas_group = pygame.sprite.Group()
        self.score_text = text_canvas(
            self.canvas_group,
            position= pygame.Vector2(WIDTH -32, 32),
            font_size= 50,
            font_path= FONT_PATH,
            anchor= 'topright'
        )
    
    # @debug(spacing= 16)
    def render(
        self,
        debug_surface:pygame.Surface = None,
    ) -> None:
        self.screen.fill(BACKGROUND_BLACK)
        self.screen.blit(debug_surface, (0, 0)) if debug_surface else None

        self.environment_group.draw(self.screen)
        self.bird_group.draw(self.screen)
        self.ground_group.draw(self.screen)
        self.canvas_group.draw(self.screen)
        
    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.bird.handling_input(event)
            if event.type == self.environment_event:
                self.add_air()
        
    def update(self, deltaTime: float) -> None:
        self.bird_group.update(deltaTime)
        self.environment_group.update(deltaTime)
        self.ground_group.update(deltaTime)

        self._send_ground_signal()
        
        self.score_text.text = f'Score: {self.score//2}'
        self.score_text.render()
        for x in self.ground_group.sprites():
            self.score += x.check_score(self.bird.rect)
    
    def add_air(self) -> None:
        for _ in range(5):
            Environment(
                self.environment_group,
                pygame.Vector2(WIDTH+16, randint(16, HEIGHT-16)),
                anchor='center',
                speed= uniform(10.5, 50),
                frames= BACKGROUND_AIR,
            )

    def new_generate_ground(
        self,
        x_coordinate: int,
        ground_group: pygame.sprite.Group,
        gap_in_tiles: int = 5,
        alpha: int = 255,
        scale: float = 1.0,
    ) -> None:
        assert alpha in range(1, 256), "Exception message raised because parameter 'alpha' is not between 0 - 255"
        
        scaled_tile_height = TILE_SIZE.y * scale
        total_tiles = int(HEIGHT//scaled_tile_height)
        max_top_tiles = int(total_tiles - (gap_in_tiles+1))
        top_tiles = randrange(1, max_top_tiles)
        bottom_tiles = total_tiles - (top_tiles+gap_in_tiles)
        # print(
        #     f"total_tiles: {total_tiles}\nmax_top_tiles: {max_top_tiles}\ntop_tiles,bottom_tiles: {top_tiles, bottom_tiles}"
        # )
        
        common_kwargs = {
            "groups": ground_group,
            "_mask": MASKS,
            "_tile_mask": TILE_MASK,
            "_ground_tileset": TILE_SET,
            "scale": scale,
            "alpha": alpha,
            "speed": self.speed,
        }
        
        top_ground = Ground(
            **common_kwargs,
            height_width= (top_tiles, 9),
            position= pygame.Vector2(x_coordinate, 0)
        )
        top_ground.image = pygame.transform.flip(top_ground.image, False, True)
        Ground(
            **common_kwargs,
            height_width= (bottom_tiles, 9),
            position= pygame.Vector2(x_coordinate, HEIGHT),
            anchor= "bottomleft"
        )
        # print(len(self.ground_group.sprites()))
    
    def masked_collision_check(
            self
    ) -> bool:
        return pygame.sprite.spritecollide(self.bird, self.ground_group, False, pygame.sprite.collide_mask)

    def _send_ground_signal(self) -> None:
        """Check if we should emit the signal."""
        if self.ground_group.sprites():
            last_ground: Ground = self.ground_group.sprites()[-1]
            if int(last_ground.position.x) == WIDTH - last_ground.image.get_width():
                ground_signal.emit()
    
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
