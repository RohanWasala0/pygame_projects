from random import choice, randint
from dataclasses import dataclass
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
        
        self.group = groups
        self.position = position
        self.velocity = Vector2(-1, 0) * speed
        self.anchor = anchor
        self.input_chart = {}
        self.tile_width, self.tile_height = ground_tiles[0].size
        
        @dataclass
        class Tile: tile: List[Surface]; connections: Dict[str, List]

        self.Ground = {
            'corner_topleft': Tile([ground_tiles[0]], {
                'topleft': None,
                'top': ['foliage'],
                'topright': ['stright_left', 'corner_topleft'],
                'left': ['foliage'],
                'right': ['dirt'],
                'buttomleft': ['corner_topleft', 'stright_top'],
                'buttom': ['dirt'],
                'buttomright': ['dirt'] 
            }),
            'corner_topright': Tile([ground_tiles[10]], {
                'topright': None,
                'top': ['foliage'],
                'topleft': ['stright_right', 'corner_topright'],
                'right': ['foliage'],
                'left': ['dirt'],
                'buttomright': ['corner_topright', 'stright_top'],
                'buttom': ['dirt'],
                'buttomleft': ['dirt'] 
            }),
            'corner_buttomleft': Tile([ground_tiles[4]], {
                'buttomleft': None,
                'buttom': ['foliage'],
                'buttomright': ['stright_left', 'corner_buttomleft'],
                'left': ['foliage'],
                'right': ['dirt'],
                'topleft': ['corner_buttomleft', 'stright_buttom'],
                'top': ['dirt'],
                'topright': ['dirt'] 
            }),
            'corner_bottomright': Tile([ground_tiles[14]], {
                'bottomright': None,
                'bottom': ['foliage'],
                'bottomleft': ['stright_right', 'corner_bottomright'],
                'right': ['foliage'],
                'left': ['dirt'],
                'topright': ['corner_buttomright', 'stright_buttom'],
                'top': ['dirt'],
                'topleft': ['dirt']
            }),
            'stright_top': Tile([ground_tiles[5]], {
                'topleft': None,
                'top': ['foliage'],
                'topright': None,
                'left': ['corner_topleft'],
                'right': ['corner_topright'],
                'bottomleft': ['dirt', 'stright_left'],
                'bottom': ['dirt'],
                'bottomright': ['dirt', 'stright_right']
            }),
            'stright_bottom': Tile([ground_tiles[9]], {
                'bottomleft': None,
                'bottom': ['foliage'],
                'bottomright': None,
                'left': ['corner_buttomleft'],
                'right': ['corner_buttomright'],
                'topleft': ['dirt', 'stright_left'],
                'top': ['dirt'],
                'topright': ['dirt', 'stright_right']
            }),
            'stright_left': Tile([ground_tiles[1], ground_tiles[2], ground_tiles[3]], {
                'topleft': ['corner_buttomleft', 'foliage'],
                'top': ['corner_topleft', 'stright_left'],
                'topright': ['dirt'],
                'left': ['foliage'],
                'right': ['dirt'],
                'bottomleft': ['corner_topleft', 'foliage'],
                'bottom': ['corner_topleft', 'stright_left'],
                'bottomright': ['dirt']
            }),
            'stright_right': Tile([ground_tiles[11], ground_tiles[12], ground_tiles[13]], {
                'topright': ['corner_buttomright', 'foliage'],
                'top': ['corner_topright', 'stright_right'],
                'topleft': ['dirt'],
                'right': ['foliage'],
                'left': ['dirt'],
                'bottomright': ['corner_topright', 'foliage'],
                'bottom': ['dirt', 'stright_right'],
                'bottomleft': ['dirt']
            }),
            'dirt': Tile([ground_tiles[6], ground_tiles[7], ground_tiles[8]], {
                'topleft': ['dirt', 'corner_topleft', 'stright_left'],
                'top': ['dirt', 'anchor', 'stright_top'],
                'topright': ['dirt', 'corner_topright', 'stright_right'],
                'left': ['dirt', 'stright_left'],
                'right': ['dirt', 'stright_right'],
                'bottomleft': ['dirt', 'corner_bottomleft', 'stright_left'],
                'bottom': ['dirt', 'stright_bottom'],
                'bottomright': ['dirt', 'corner_bottomright', 'stright_right']
            }),
            'foliage': Tile(foliage_tiles, {
                'topleft': ['foliage'],
                'top': ['foliage'],
                'topright': ['foliage'],
                'left': ['foliage', 'corner_topleft', 'corner_bottomleft', 'stright_left'],
                'right': ['foliage', 'corner_topright', 'corner_bottomright', 'stright_right'],
                'bottomleft': ['foliage'],
                'bottom': ['foliage'],
                'bottomright': ['foliage']
            })
        }
        
        self.image: Surface = Surface((0, 0), SRCALPHA)
        self.image.set_colorkey(Color(0, 0, 0, 0))
        self.rect: Rect = self.image.get_rect()

        self.generated_tiles = self._generate_ground(height)
        self.render()

        
    def _generate_ground(self, height: int) -> List[List[Surface]]:
        ground_tiles: List[List[Surface]] = [[Surface(((16, 16))) for _ in range(9)] for _ in range(height)]
        middle_height = height - 4 if height > 4 else 0
        
        ground_tiles[1] = [
            None, None,
            transform.rotate(choice(self.Ground['foliage'].tile), 90),
            choice(self.Ground['corner_topleft'].tile),
            choice(self.Ground['stright_top'].tile),
            choice(self.Ground['corner_topright'].tile),
            transform.rotate(choice(self.Ground['foliage'].tile), -90),
            None, None
        ]
        
        # Middle rows - consistent structure with proper edge tiles
        middle_rows = []
        for _ in range(middle_height):
            middle_rows.append([
                transform.rotate(self.get_random_tile('foliage')['tile'], 90),
                self.get_random_tile('stright_left')['tile'],
                self.get_random_tile('dirt')['tile'],
                self.get_random_tile('stright_right')['tile'],
                transform.rotate(self.get_random_tile('foliage')['tile'], -90)
            ])

        # Last 3 rows - gradually expanding mountain with proper corners
        last3_rows = []
        left_expansion = right_expansion = 0
        
        for i in range(3):
            # Base structure similar to middle rows
            row = [
                transform.rotate(self.get_random_tile('foliage')['tile'], 90),
            ]
            
            # Left edge always has a proper corner or straight piece
            if i == 0:  # First expansion row
                row.append(self.get_ground_tile('corner')['left']['tile'])
            else:
                row.append(self.get_random_tile('stright_left')['tile'])
            
            # Add dirt tiles in the middle
            # Calculate expansions - each row can expand more than the previous
            if i > 0:
                left_expansion = randint(left_expansion, min(3, left_expansion + 2))
                right_expansion = randint(right_expansion, min(3, right_expansion + 2))
            
            # Add left expansion dirt tiles
            for _ in range(left_expansion):
                row.append(self.get_random_tile('dirt')['tile'])
            
            # Add center dirt tile
            row.append(self.get_random_tile('dirt')['tile'])
            
            # Add right expansion dirt tiles
            for _ in range(right_expansion):
                row.append(self.get_random_tile('dirt')['tile'])
            
            # Right edge always has a proper corner or straight piece
            if i == 0:  # First expansion row
                row.append(self.get_ground_tile('corner')['right']['tile'])
            else:
                row.append(self.get_random_tile('stright_right')['tile'])
            
            # Add foliage at the end
            row.append(transform.rotate(self.get_random_tile('foliage')['tile'], -90))
            
            last3_rows.append(row)

        # Combine all rows
        # ground_tiles = [top_row] + middle_rows + last3_rows
        return ground_tiles


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
        self.rect.centerx = self.position.x
        self.rect.y = self.position.y
    
    def render(self):
        self.image = self.merge_tiles(self.generated_tiles)
        self.image.convert_alpha()
        
        draw.circle(self.image, Color('red'), (0, 0), radius=1)
        
        self.rect = self.image.get_rect()
        # setattr(self.rect, self.anchor, self.position)
        print('position', self.position)
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