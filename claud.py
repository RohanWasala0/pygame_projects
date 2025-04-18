import pygame
import os
import random
import noise
from dataclasses import dataclass
from typing import List, Dict, Optional

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
tile_size = 16
tiles_x, tiles_y = SCREEN_WIDTH // tile_size, SCREEN_HEIGHT // tile_size

@dataclass
class Tile:
    images: List[pygame.Surface]
    connections: Dict[str, List[str]]

class TileMap:
    def __init__(self, width: int, height: int, tile_dict: Dict[str, Tile]):
        self.width = width
        self.height = height
        self.tile_dict = tile_dict
        self.grid = self._generate_mountainous_terrain()

    def _generate_mountainous_terrain(self) -> List[List[Optional[str]]]:
        grid = [['empty' for _ in range(self.width)] for _ in range(self.height)]
        scale = 20.0
        for x in range(self.width):
            height = int(noise.pnoise1(x / scale, octaves=4) * (self.height // 3) + (self.height // 2))
            for y in range(height, self.height):
                grid[y][x] = 'dirt' if y > height else 'mountain'
        return grid

    def draw(self, screen: pygame.Surface):
        for y, row in enumerate(self.grid):
            for x, tile_type in enumerate(row):
                if tile_type and tile_type in self.tile_dict:
                    screen.blit(random.choice(self.tile_dict[tile_type].images), (x * tile_size, y * tile_size))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.tile_dict = self._load_tiles()
        self.tile_map = TileMap(tiles_x, tiles_y, self.tile_dict)
        self.running = True

    def _load_tiles(self) -> Dict[str, Tile]:
        ground_tiles = [pygame.image.load(entry.path) for entry in os.scandir('./PyBird/assets/Retro-Lines-16x16/ground_tiles')]
        foliage = pygame.Surface((tile_size, tile_size))
        pygame.draw.rect(foliage, pygame.Color('red'), foliage.get_rect())
        foliage_tiles = [foliage] * 5
        return {
            'dirt': Tile(ground_tiles[6:9], {'top': ['dirt', 'mountain']}),
            'mountain': Tile([ground_tiles[3]], {'top': ['mountain', 'foliage']}),
            'foliage': Tile(foliage_tiles, {'bottom': ['mountain']}),
            'empty': Tile([pygame.Surface((16, 16))], {})
        }

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.tile_map.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    Game().run()
