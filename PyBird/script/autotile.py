from pygame import Vector2, Surface, transform
from typing import List, Union, Tuple, Dict, Optional
from random import choice 

class Tile:
    def __init__(
            self,
            mask: List[List[int]],
            image: Union[Surface, List[Surface]],
    ):
        """Tile class represents a single tile with a connectivity mask and image

        Args:
            mask (List[List[int]]): 3x3 grid indicating the connectivity of the tile.
            image (Union[Surface, List[Surface]]): Surface or List of Surfaces representing tile sprite.
        """
        self.mask = mask
        self.image = image

    def draw(
            self,
            screen: Surface,
            blit_position: Vector2,
    ) -> None:
        """Blit the tile image on the screen at the given position

        Args:
            screen (Surface): The Surface to blit on to 
            blit_position (Vector2): The position to blit the tile image at
        """
        image_to_blit = self.image if isinstance(self.image, Surface) else choice(self.image)
        screen.blit(image_to_blit, blit_position)

class AutoTile:
    def __init__(
            self,
            tileset: Surface,
            tile_mask: List[List[int]],
            mask_template: List[List[int]],
    ):
        """AutoTile handles automatic selection of tiles based on the adjacent tiles

        Args:
            tileset (Surface): Surface containing the full tilemap
            tile_mask (List[List[int]]): 2D grid marking which tiles are used 
            mask_template (List[List[int]]): 2D Template defining 3x3 connectivity for each tile
        """
        self.tileset: Surface = tileset
        self.tile_size: Vector2 = Vector2(
            self.tileset.width//len(tile_mask[0]), 
            self.tileset.height//len(tile_mask)
        )
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

        self._generate_tiles(tile_mask, mask_template)

    def _generate_tiles(
            self,
            tile_mask: List[List[int]],
            mask_template: List[List[int]],
    ) -> None:
        """Generate tiles Tiles class objects based on tile_mask and mask_template"""
        tile_by_mask: Dict[Tuple, List[Surface]] = {}

        for y, row in enumerate(tile_mask):
            for x, tile in enumerate(row):
                if tile == 1:
                    single_tile_mask = []
                    for i in range(3):
                        row_start = x*3
                        row_end = x*3 +3
                        if y*3+i < len(mask_template) and row_end <= len(mask_template[y*3+i]):
                            single_tile_mask.append(mask_template[y * 3 + i][row_start:row_end])
                        else:
                            single_tile_mask.append([0, 0, 0])

                    mask_key = tuple(tuple(row) for row in single_tile_mask)
                    tile_surface = self.make_tile_surface(Vector2(x, y))
                    tile_by_mask.setdefault(mask_key, []).append(tile_surface)
                    
        for mask in tile_by_mask.keys():
            list_mask = [list(row) for row in mask]
            self.tiles.append(Tile(list_mask, tile_by_mask[mask]))

    def make_tile_surface(
            self,
            position: Vector2,
            scale: float = 1,
    ) -> Surface:
        """Cuts, Scales a Surface from the tilemap to make tile sprite 
        Returns:
            Surface: The tile sprite as a surface scaled to factor 
        """
        x, y = position.x* self.tile_size.x, position.y* self.tile_size.y
        tile: Surface = Surface((self.tile_size.x, self.tile_size.y))
        tile.blit(
            self.tileset,
            (0, 0),
            (x, y, self.tile_size.x, self.tile_size.y)
        )
        # return transform.scale(tile, (tile.width* scale, tile.height* scale))
        return tile

    def get_tile(
            self,
            mask: List[List[int]],
    ) -> Surface:
        """Finds a tile matching a specific 3x3 match
        Returns:
            The matching Tile or None if not found
        """
        for tile in self.tiles:
            if mask == tile.mask:
                return tile
        return None

    def generate_connectivity_mask(
            self,
            tile_map: List[List[int]],
            position: Vector2,
            width: int, height: int
    ) -> List[List[int]]:
        """Generates a 3x3 connectivity mask for a given tile position 
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
                    
                    out_of_bounds = not (0 <= nx < width and  0 <= ny < height)
                    direction = self._get_direction(nx, ny)
                    # Check if the position is within bounds and has a tile
                    if out_of_bounds:
                        if direction == "above":
                            is_connected = False
                        elif direction == "below":
                            is_connected = True
                        elif direction in ("left", "right"):
                            is_connected = int(position.y) == height -1 
                    else:
                        if tile_map[ny][nx] == 0:
                            is_connected = False
                
                if is_connected and directions:  # Only set to 1 if there are directions to check
                    mask[my][mx] = 1
                    
        return mask

    def _get_direction(
            self,
            dx: int, dy: int,
    ) -> str:
        """Helper function 
        Converts a directional offset into a string

        Args:
            dx (int): X offset
            dy (int): Y offset      

        Returns:
            str: A string representing direction 
        """
        if dy == -1: return "above"
        if dy == 1: return "below"
        if dx == -1: return "left"
        if dx == 1: return "right"
        return "unknown"
