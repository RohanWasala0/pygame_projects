from random import choice
from pygame import sprite, Vector2, event, Rect, Color, Surface, SRCALPHA, draw, transform, mask, display
from typing import List, Optional, Dict, Union

class Ground(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                anchor: str = 'topleft',
                height: int = 3,
                frames: list = [],
                ) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.position = Vector2(position.x - 24, position.y)
        self.velocity = Vector2(-1, 0) * 25
        self.anchor = anchor
        self.input_chart = {}
        self.ground_tiles = []
        
        self.GROUND = {
            "corner": {
                'left': {'frame': frames[0], 'tile_map': [[0, 0, 0], [0, 'corner', 'anchor'], [0, 'stright_left', 'dirt']]},
                'right': {'frame': frames[10], 'tile_map': [[0, 0, 0], ['anchor', 'corner', 0], ['dirt', 'stright_right', 0]]},
            },
            "anchor": {'frame': frames[5], 'tile_map': [[0, 0, 0], ['corner_left', 'anchor', 'corner_right'], ['stright_left', 'dirt', 'stright_right']]},
            "stright": {
                'left': {'frame': [frames[1], frames[2], frames[3]], 'tile_map': [[0, 'corner_left', 'anchor'], [0, 'stright_left', 'dirt'], [0, 'stright_left', 'dirt']]},
                'right': {'frame': [frames[11], frames[12], frames[13]], 'tile_map': [[0, 'corner_right', 'anchor'], [0, 'stright_right', 'dirt'], [0, 'stright_right', 'dirt']]},
            },
            "dirt": {'frame': [frames[6], frames[7], frames[8]]},
        }
        
        self.image: Surface = Surface((0, 0), SRCALPHA)
        self.image.set_colorkey(Color(0, 0, 0, 0))
        self.rect: Rect = self.image.get_rect()
        # setattr(self.rect, self.anchor, self.position)

        self.generated_tiles = self._generate_standard_ground(3, height)
        # self.generate_tiles()

        self.render()

    def generate_tiles(self) -> None:
        start_tiles = [[self.GROUND['anchor']]]
        self.generated_tiles = []
        for y in range(len(start_tiles)):
            for x in start_tiles[y]:
                map = x['tile_map']
                layer = []
                for k in map:
                    if 0 in k:
                        continue
                    else:
                        for x in k:
                            layer.append(self.get_ground_tile(x)['frame'])
                self.generated_tiles.append(layer)
        
    def _generate_standard_ground(self, width: int, height: int) -> List[List[Surface]]:
        """
        Generate a standard ground layout with anchor, corners, and dirt tiles.
        """
        ground_tiles = []
        
        # First row (top layer)
        top_row = [
            self.get_ground_tile('corner_left')['frame'],
            self.get_ground_tile('anchor')['frame'],
            self.get_ground_tile('corner_right')['frame']
        ]
        
        # Middle rows (dirt)
        middle_rows =[
            [self.get_random_tile('stright_left')['frame'],
            self.get_random_tile('dirt')['frame'],
            self.get_random_tile('stright_right')['frame']]
         for _ in range(height)]
        
        ground_tiles = [top_row] + middle_rows
        return ground_tiles

    def get_random_tile(self, tile_category: str) -> Dict[str, Union[List[Surface], Surface]]:
        """
        Get a random tile from a specific category.
        """
        tile_data = self.get_ground_tile(tile_category)
        if isinstance(tile_data['frame'], list):
            return {'frame': choice(tile_data['frame'])}
        return tile_data

    def get_ground_tile(self, tile_name):
        keys = tile_name.split("_")  # Split the string by "_"

        if len(keys) == 1:  # Direct key lookup (e.g., "anchor" or "dirt")
            return self.GROUND.get(keys[0], None)

        if len(keys) == 2:  # Nested lookup (e.g., "corner_right" -> self.GROUND["corner"]["right"])
            main_key, sub_key = keys
            return self.GROUND.get(main_key, {}).get(sub_key, None)

        return None  # Return None if the format is unexpected 

    def merge_tiles(self, ground_tiles) -> Surface:
        x = len(ground_tiles[0])
        y = len(ground_tiles)
        ground = Surface((x*16, y*16), SRCALPHA)
        for y, tile_row in enumerate(ground_tiles):
            for x, tile in enumerate(tile_row):
                if type(tile) == Surface:
                    ground.blit(tile, (x*16, y*16))
                else:
                    ground.blit(choice(tile), (x*16, y*16))
        return ground

    def update(self, deltaTime: float):
        self.kill() if self.position.x + self.image.width//2 < 0 else None
        
        position = self.position + (self.velocity * deltaTime)
        self.position = self.position.smoothstep(position, 0.6)
        setattr(self.rect, self.anchor, self.position)
    
    def render(self):
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        tile = self.merge_tiles(self.generated_tiles)
        # size = (40*3, 40*3)
        # self.image = transform.scale(tile, size)
        self.image = tile
        
        draw.circle(self.image, Color('white'), (self.image.get_rect().x, self.image.get_rect().y), 3)

        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
    
    def testing(self, ENVIRONMENT_SHEET) -> list:
        ENVIRONMENT_SHEET_list = []
        for y in range(ENVIRONMENT_SHEET.get_height()//16):
            for x in range(ENVIRONMENT_SHEET.get_width()//16):
                ENVIRONMENT_SHEET_list.append(ENVIRONMENT_SHEET.subsurface((16*x, 16*y, 16, 16)))
        
        for x in ENVIRONMENT_SHEET_list[:]:  # Iterate over a copy to avoid modifying the list while iterating
            if mask.from_surface(x).count() == 0:
                ENVIRONMENT_SHEET_list.remove(x)
        return ENVIRONMENT_SHEET_list