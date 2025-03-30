from random import choice, randint
from pygame import sprite, Vector2, event, Rect, Color, Surface, SRCALPHA, draw, transform, mask, display
from typing import List, Optional, Dict, Union

class Ground(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                anchor: str = 'topleft',
                height: int = 3,
                ground_tiles: List[Surface] = None,
                foliage_tiles: List[Surface] = None,
                speed: float = 10.0,
                ) -> None:
        super().__init__(groups)
        
        # ground_tiles = [transform.scale(x, [y* 1.5 for y in x.size]) for x in ground_tiles]
        # foliage_tiles = [transform.scale(x, [y* 0.7 for y in x.size]) for x in foliage_tiles]

        self.group = groups
        self.position = position
        self.velocity = Vector2(-1, 0) * speed
        self.anchor = anchor
        self.input_chart = {}
        self.tile_width, self.tile_height = ground_tiles[0].size
        
        self.GROUND = {
            "corner": {
                'left': {'tile': ground_tiles[0], 'tile_map': [[0, 'foliage', 0], ['foliage', 'corner', 'anchor'], ['foliage', 'stright_left', 'dirt']]},
                'right': {'tile': ground_tiles[10], 'tile_map': [[0, 0, 0], ['anchor', 'corner', 0], ['dirt', 'stright_right', 0]]},
            },
            "anchor": {'tile': ground_tiles[5], 'tile_map': [[0, 0, 0], ['corner_left', 'anchor', 'corner_right'], ['stright_left', 'dirt', 'stright_right']]},
            "stright": {
                'left': {'tile': [ground_tiles[1], ground_tiles[2], ground_tiles[3]], 'tile_map': [[0, 'corner_left', 'anchor'], [0, 'stright_left', 'dirt'], [0, 'stright_left', 'dirt']]},
                'right': {'tile': [ground_tiles[11], ground_tiles[12], ground_tiles[13]], 'tile_map': [[0, 'corner_right', 'anchor'], [0, 'stright_right', 'dirt'], [0, 'stright_right', 'dirt']]},
            },
            "dirt": {'tile': [ground_tiles[6], ground_tiles[7], ground_tiles[8]]},
            "foliage": {'tile': foliage_tiles},
        }
        
        self.image: Surface = Surface((0, 0), SRCALPHA)
        self.image.set_colorkey(Color(0, 0, 0, 0))
        self.rect: Rect = self.image.get_rect()

        self.generated_tiles = self._generate_ground(height)
        self.render()

        
    def _generate_ground(self, height: int) -> List[List[Surface]]:
        ground_tiles = []
        middle = height - 4 if height > 4 else 0
        top_row = [
            transform.rotate(self.get_random_tile('foliage')['tile'], 90),
            self.get_ground_tile('corner_left')['tile'],
            self.get_ground_tile('anchor')['tile'],
            self.get_ground_tile('corner_right')['tile'],
            transform.rotate(self.get_random_tile('foliage')['tile'], -90)
        ]
        
        middle_rows =[[
            transform.rotate(self.get_random_tile('foliage')['tile'], 90),
            self.get_random_tile('stright_left')['tile'],
            self.get_random_tile('dirt')['tile'],
            self.get_random_tile('stright_right')['tile'],
            transform.rotate(self.get_random_tile('foliage')['tile'], -90)
        ]for _ in range(middle)]

        left_extra, right_extra = 0, 0
        last3_rows = []
        for x in range(1, 4):
            row = [
                transform.rotate(self.get_random_tile('foliage')['tile'], 90),
                self.get_random_tile('stright_left')['tile'],
                self.get_random_tile('dirt')['tile'],
                self.get_random_tile('stright_right')['tile'],
                transform.rotate(self.get_random_tile('foliage')['tile'], -90)
            ]
            left_extra = randint(left_extra, 4)
            for _ in range(left_extra):
                row.insert(2, self.get_random_tile('dirt')['tile'])
            
            right_extra = randint(right_extra, 4)
            for _ in range(right_extra):
                row.insert(-2, self.get_random_tile('dirt')['tile'])
            last3_rows.append(row)
            print(len(row))

        ground_tiles = [top_row] + middle_rows + last3_rows
        return ground_tiles

    def get_random_tile(self, tile_category: str) -> Dict[str, Union[List[Surface], Surface]]:

        tile_data = self.get_ground_tile(tile_category)
        if isinstance(tile_data['tile'], list):
            return {'tile': choice(tile_data['tile'])}
        return tile_data

    def get_ground_tile(self, tile_name):
        keys = tile_name.split("_")  

        if len(keys) == 1:  # Direct key lookup (e.g., "anchor" or "dirt")
            return self.GROUND.get(keys[0], None)

        if len(keys) == 2:  # Nested lookup (e.g., "corner_right" -> self.GROUND["corner"]["right"])
            main_key, sub_key = keys
            return self.GROUND.get(main_key, {}).get(sub_key, None)

        return None  

    # def merge_tiles(self, tiles) -> Surface:
    #     ground = Surface((len(max(tiles, key=len))*self.tile_width, len(tiles)*self.tile_height), SRCALPHA)
    #     for y, tile_row in enumerate(tiles):
    #         for x, tile in enumerate(tile_row):
    #             ground.blit(tile, (x* self.tile_width, y* self.tile_height ))
    #     return ground

    def merge_tiles(self, tiles) -> Surface:
    # Find the longest row to determine the width of the surface
        max_row_length = len(max(tiles, key=len))
        
        # Find the anchor position (index 2 in the top row)
        anchor_position = 2
        
        # Create the surface with the maximum possible width
        ground = Surface((max_row_length * self.tile_width, len(tiles) * self.tile_height), SRCALPHA)
        
        for y, tile_row in enumerate(tiles):
            # Calculate offset for centering the current row relative to the anchor
            # The idea is to keep the anchor tile (or where it would be) centered
            row_center_offset = (max_row_length - len(tile_row)) // 2
            
            # Additional offset to align with the anchor position (not the center of the row)
            anchor_alignment_offset = anchor_position - (len(tiles[0]) // 2)
            
            # Combined offset
            offset = row_center_offset + anchor_alignment_offset
            
            for x, tile in enumerate(tile_row):
                ground.blit(tile, ((x + offset) * self.tile_width, y * self.tile_height))
        
        return ground

    def update(self, deltaTime: float):
        self.kill() if self.position.x + self.image.width//2 < 0 else None
        
        position = self.position + (self.velocity * deltaTime)
        self.position = self.position.smoothstep(position, 0.6)
        setattr(self.rect, self.anchor, self.position)
    
    def render(self):
        self.image = self.merge_tiles(self.generated_tiles)
        self.image.convert_alpha()
        
        draw.circle(self.image, Color('red'), (0, 0), radius=1)
        
        self.rect = self.image.get_rect()
        # setattr(self.rect, self.anchor, self.position)
        self.rect.centerx = self.position.x
        self.rect.y = self.position.y
    
    # def generate_tiles(self) -> None:
    #     start_tiles = [[self.GROUND['anchor']]]
    #     self.generated_tiles = []
    #     for y in range(len(start_tiles)):
    #         for x in start_tiles[y]:
    #             map = x['tile_map']
    #             layer = []
    #             for k in map:
    #                 if 0 in k:
    #                     continue
    #                 else:
    #                     for x in k:
    #                         layer.append(self.get_ground_tile(x)['tile'])
    #             self.generated_tiles.append(layer)