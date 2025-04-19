from pygame import Vector2, Surface, transform
from typing import List, Union
from random import choice 

class Tile:
    def __init__(
            self,
            position: Vector2 = Vector2(),
            mask: List[List[int]] = [],
            image: Union[Surface, List[Surface]] = Surface,
    ):
        """
        Args:
            position: position in the tileset
            mask: 3x3 grid representing which sides connect
            image: The pygame Surface for this tile
        """
        self.mask = mask
        self.image = image

    def draw(
            self,
            screen: Surface,
            blit_position: Vector2,
    ) -> None:
        if isinstance(self.image, Surface):
            screen.blit(self.image, blit_position)
        elif isinstance(self.image, list):
            screen.blit(choice(self.image), blit_position)

class AutoTile:
    def __init__(
            self,
            tileset: Surface,
            tile_size: int,
            scale: float,
            tile_mask: List[List[int]],
            mask: List[List[int]],
    ):
        self.tileset = transform.scale(tileset, (tileset.width*scale, tileset.height*scale))
        self.tile_size = tile_size
        self.tiles: List[Tile] = []

        self.directions = [
            [   # Top row
                [[-1, 0], [-1, -1], [0, -1]],   # Top-left checks left, up-left, and up
                [[0, -1]],                      # Top-center checks only up
                [[1, 0], [1, -1], [0, -1]]      # Top-right checks right, up-right, and up
            ],
            [   # Middle row
                [[-1, 0]],                      # Middle-left checks only left
                [],                             # Center (self)
                [[1, 0]]                        # Middle-right checks only right
            ],
            [   # Bottom row
                [[-1, 0], [-1, 1], [0, 1]],     # Bottom-left checks left, down-left, and down
                [[0, 1]],                       # Bottom-center checks only down
                [[1, 0], [1, 1], [0, 1]]        # Bottom-right checks right, down-right, and down
            ]
        ]

        tile_by_mask = {}
        for y, row in enumerate(tile_mask):
            for x, tile in enumerate(row):
                if tile==1:
                    single_tile_mask = []
                    for i in range(3):
                        row_start = x*3
                        row_end = x*3 +3
                        if y*3+i < len(mask) and row_end <= len(mask[y*3+i]):
                            single_tile_mask.append(mask[y * 3 + i][row_start:row_end])
                        else:
                            single_tile_mask.append([0, 0, 0])
                    
                    tile_surface = Surface((self.tile_size, self.tile_size))
                    tile_surface.blit(
                        self.tileset, 
                        (0, 0), 
                        (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    )
                    mask_key = tuple(tuple(row) for row in single_tile_mask)
                    if mask_key not in tile_by_mask:
                        tile_by_mask[mask_key] = []
                    tile_by_mask[mask_key].append(tile_surface)
                    
                    #self.tiles.append(Tile(Vector2(x, y), single_tile_mask, tile_surface))
        for mask in tile_by_mask.keys():
            list_mask = [list(row) for row in mask]
            self.tiles.append(Tile(Vector2(x, y), list_mask, tile_by_mask[mask]))
            
        # print([h.mask for h in self.tiles])
        
    def get_tile(
            self,
            mask: List[List[int]],
    ) -> Surface:
        """
        Returns:
            The matching Tile or None if not found
        """
        for tile in self.tiles:
            if mask == tile.mask:
                return tile
        return None

    def generate_conectivity_mask(
            self,
            tile_map: List[List[int]],
            position: Vector2,
            width: int, height: int
    ) -> List[List[int]]:
        """ 
        Returns:
            A 3x3 mask representing connections to adjacent tiles
        """
        mask = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        
        for my in range(3):
            for mx in range(3):
                # Get all directions to check for this grid position
                directions = self.directions[my][mx]
                is_connected = True
                
                for dx, dy in directions:
                    nx, ny = int(position.x + dx), int(position.y + dy)
                    
                    # Check if the position is within bounds and has a tile
                    if 0 <= nx < width and 0 <= ny < height:
                        if tile_map[ny][nx] == 0:
                            is_connected = False
                    else:
                        # Out of bounds counts as no connection
                        is_connected = False
                
                if is_connected and directions:  # Only set to 1 if there are directions to check
                    mask[my][mx] = 1
                    
        return mask

