from pygame import sprite, Surface, Vector2, draw, Color, SRCALPHA, Rect, transform
from script.autotile import AutoTile, Tile
from random import choice
from typing import List, Tuple


class Ground(sprite.Sprite):
    def __init__(
            self,
            groups: sprite.Group,
            position: Vector2,
            height_weidth: Tuple[int, int],
            scale: float,
            ground_tilemap: Surface,
            tile_mask: List[List[int]],
            mask: List[List[int]],
    ) -> None:
        super().__init__(groups)
        self.group = groups
        self.position: Vector2 = position or Vector2()
        self.velocity: Vector2 = Vector2(-1, 0)* 35
        self.autotile: AutoTile = AutoTile(ground_tilemap, 16*scale, scale, tile_mask, mask)
        self.height, self.width = height_weidth

        self.render()

    def _pregenerate_tile_map(
            self,
            width: int,
            height: int,
    ) -> List[List[int]]:
        
        ground_tiles: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]
        temp = 0
        if width < height:
            for x in range(height-width):
                ground_tiles[x] = [0] * ((width - 3) // 2) + [1, 1, 1] + [0] * ((width - 3) // 2)
            temp = height-width

        center = width//2
        left = center -1
        right = center +1
        for i in range(temp, height-1):
            row = []
            for j in range(width):
                if left <= j <= right:
                    row.append(1)
                else:
                    row.append(0)
            if left > 0:
                left -= choice([0, 1])
            if right < width -1:
                right += choice([0, 1])
            # print(row)

            ground_tiles[i] = row
        ground_tiles[height-1] = [1]*width
        return ground_tiles

    def _generate_ground(
            self,
            tile_map: List[List[int]],
    ) -> Surface:
        
        map_height = len(tile_map)
        map_width = len(tile_map[0]) if map_height>0 else 0
        print(map_height, map_width)
        surface = Surface((map_width*self.autotile.tile_size, map_height*self.autotile.tile_size), SRCALPHA)

        for y, row in enumerate(tile_map):
            for x, cell in enumerate(row):
                if cell == 1:
                    mask = self.autotile.generate_conectivity_mask(tile_map, Vector2(x, y), map_width, map_height)

                    tile: Tile = self.autotile.get_tile(mask)
                    if tile:
                        tile.draw(surface, Vector2(x* self.autotile.tile_size, y* self.autotile.tile_size))
                    else:
                        if self.autotile.tiles:
                            fallback_tile: Tile = self.autotile.tiles[8]
                            fallback_tile.draw(surface, Vector2(x* self.autotile.tile_size, y* self.autotile.tile_size)) 
        return surface

    def _display_tiles(
            self
    ) -> Surface:
        surface: Surface = Surface((self.autotile.tile_size*5, self.autotile.tile_size*5))
        matrix = [self.autotile.tiles[i:i+5] for i in range(0, 25, 5)]
        for y, row in enumerate(matrix):
            for x, tile in enumerate(row):
                surface.blit(tile.image, (x*self.autotile.tile_size, y*self.autotile.tile_size))
                print(f'at:({x},{y})\nmask:{tile.mask}')
        return surface
    
    def update(self, deltaTime: float):
        self.kill() if self.position.x + self.image.width//2 < 0 else None
        
        position = self.position + (self.velocity * deltaTime)
        self.position = self.position.smoothstep(position, 0.6)
        self.rect.centerx = self.position.x
        self.rect.y = self.position.y
    
    def render(self):
        self.tile_map = self._pregenerate_tile_map(self.width, self.height)
        self.image: Surface = self._generate_ground(self.tile_map)
        # self.image: Surface = self._display_tiles()
        # self.image = transform.scale(self.image, (self.image.width + 16*4, self.image.height)) 
        self.image.set_colorkey(Color('black'))
        self.image.convert_alpha()
        self.rect: Rect = self.image.get_rect()
        
        draw.circle(self.image, Color('red'), (0, 0), radius=3)
        draw.rect(
            self.image,
            Color('white'),
            self.image.get_rect(),
            width= 1,
        )
        
        self.rect = self.image.get_rect()
        # setattr(self.rect, self.anchor, self.position)
        self.rect.centerx = self.position.x
        self.rect.y = self.position.y