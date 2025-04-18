import pygame as pg
import math
from typing import List, Tuple, Optional


class Tile:
    """Class representing a single tile with its mask and image."""
    
    def __init__(self, position_x: int, position_y: int, mask: List[List[int]], image: pg.Surface):
        """
        Initialize a tile.
        
        Args:
            position_x: X position in the tileset
            position_y: Y position in the tileset
            mask: 3x3 grid representing which sides connect
            image: The pygame Surface for this tile
        """
        self.mask = mask
        self.image = image
        self.position = (position_x, position_y)
    
    def draw(self, screen: pg.Surface, x: int, y: int, show_mask: bool = False) -> None:
        """
        Draw the tile at the specified position.
        
        Args:
            screen: Pygame surface to draw on
            x: X position to draw at
            y: Y position to draw at
            show_mask: Whether to overlay the mask visualization
        """
        screen.blit(self.image, (x, y))
        
        if show_mask:
            mask_surface = pg.Surface((self.image.get_width(), self.image.get_height()))
            mask_surface.set_alpha(100)
            
            cell_size = self.image.get_width() // 3
            
            for row_idx, row in enumerate(self.mask):
                for col_idx, cell in enumerate(row):
                    if cell == 1:
                        pg.draw.rect(
                            mask_surface, 
                            (255, 0, 0), 
                            (col_idx * cell_size, row_idx * cell_size, cell_size, cell_size)
                        )
            screen.blit(mask_surface, (x, y))


class AutoTile:
    """Class for handling auto-tiling logic."""
    
    def __init__(self, tileset_path: str, tile_size: int):
        """
        Initialize the AutoTile system.
        
        Args:
            tileset_path: Path to the tileset image
            tile_size: Size of each tile in pixels
        """
        self.tileset = pg.image.load(tileset_path)
        self.tile_size = tile_size
        
        # Define the edge checking directions for each position in the 3x3 grid
        self.directions = [
            [   # Top row
                [[-1, 0], [0, -1], [-1, -1]],  # Top-left
                [[0, -1]],                      # Top-center
                [[1, 0], [0, -1], [1, -1]]  # Top-right checks right, up, and up-right
            ],
            [   # Middle row
                [[-1, 0]],                      # Middle-left
                [],                             # Center (self)
                [[1, 0]]                        # Middle-right
            ],
            [   # Bottom row
                [[-1, 0], [0, 1], [-1, 1]],    # Bottom-left
                [[0, 1]],                       # Bottom-center
                [[1, 0], [0, 1], [1, 1]]        # Bottom-right
            ]
        ]
        
        # Load tile masks from hardcoded values (replace with file parsing in production)
        
        file = open('./PyBird/assets/Retro-Lines-16x16/autotile_tilemap/mask.txt').readlines()
        tile_mask = [[int(char) for char in line.strip()] for line in file[:6]]

        masks = [[int(char) for char in line.replace("\n", "").replace(" ", "")] for line in file[6:]]
        
        # Initialize tiles from the tileset
        self.tiles = []
        for y, row in enumerate(tile_mask):
            for x, tile in enumerate(row):
                if tile == 1:
                    # Extract the 3x3 mask for this tile
                    tile_mask = []
                    for i in range(3):
                        row_start = x * 3
                        row_end = x * 3 + 3
                        if y * 3 + i < len(masks) and row_end <= len(masks[y * 3 + i]):
                            print(masks[y * 3 + i][row_start:row_end])
                            tile_mask.append(masks[y * 3 + i][row_start:row_end])
                        else:
                            # Handle potential out-of-bounds with a default row
                            tile_mask.append([0, 0, 0])
                    
                    # Extract the tile image from the tileset
                    tile_surface = pg.Surface((self.tile_size, self.tile_size))
                    tile_surface.blit(
                        self.tileset, 
                        (0, 0), 
                        (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    )
                    # print(tile_mask) 
                    self.tiles.append(Tile(x, y, tile_mask, tile_surface))
        
        # print([h.mask for h in self.tiles])

    def get_tile(self, mask: List[List[int]]) -> Optional[Tile]:
        """
        Find a tile matching the given mask pattern.
        
        Args:
            mask: A 3x3 grid of 0s and 1s representing connections
            
        Returns:
            The matching Tile or None if not found
        """
        for tile in self.tiles:
            if mask == tile.mask:
                return tile
        return None
    
    def render_map(self, screen: pg.Surface, tile_map: List[List[int]], show_masks: bool = False) -> None:
        """
        Render the entire tilemap to the screen.
        
        Args:
            screen: Pygame surface to draw on
            tile_map: 2D grid of 0s and 1s indicating tile presence
            show_masks: Whether to show the mask overlays for debugging
        """
        map_height = len(tile_map)
        map_width = len(tile_map[0]) if map_height > 0 else 0
        
        for y, row in enumerate(tile_map):
            for x, cell in enumerate(row):
                if cell == 1:
                    # Generate the connectivity mask for this position
                    mask = self._generate_connectivity_mask(tile_map, x, y, map_width, map_height)
                    
                    # Get and draw the appropriate tile
                    tile = self.get_tile(mask)
                    if tile:
                        tile.draw(screen, x * self.tile_size, y * self.tile_size, show_masks)
                    else:
                        # Fallback to a default tile if no matching tile is found
                        if self.tiles:
                            fallback_tile = self.tiles[21]  # Default fallback
                            fallback_tile.draw(screen, x * self.tile_size, y * self.tile_size, show_masks)
    
    def _generate_connectivity_mask(self, tile_map: List[List[int]], x: int, y: int, 
                                   width: int, height: int) -> List[List[int]]:
        """
        Generate a 3x3 connectivity mask for the given position.
        
        Args:
            tile_map: The complete map grid
            x: X position in the map
            y: Y position in the map
            width: Width of the map
            height: Height of the map
            
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
                    nx, ny = x + dx, y + dy
                    
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


class Game:
    """Main game class to handle initialization and game loop."""
    
    def __init__(self, screen_size: Tuple[int, int] = (640, 640), 
                 map_size: Tuple[int, int] = (10, 10),
                 tile_size: int = 16):
        """
        Initialize the game.
        
        Args:
            screen_size: Size of the game window
            map_size: Size of the tile map
            tile_size: Size of each tile in pixels
        """
        pg.init()
        self.screen = pg.display.set_mode(screen_size)
        pg.display.set_caption("AutoTile Editor")
        
        # Map properties
        self.map_width, self.map_height = map_size
        self.tile_map = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        
        # Display properties
        self.screen_width, self.screen_height = screen_size
        self.tile_size = tile_size
        self.display_scale = screen_size[0] // (map_size[0] * tile_size)
        
        # Load autotile system
        self.autotile = AutoTile('./PyBird/assets/Retro-Lines-16x16/autotile_tilemap/tilemap.png', tile_size)
        
        # Game state
        self.running = True
        self.show_masks = False  # Debug option
        self.clock = pg.time.Clock()
    
    def handle_events(self) -> None:
        """Process all pygame events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    # Toggle mask visibility for debugging
                    self.show_masks = not self.show_masks
                elif event.key == pg.K_c:
                    # Clear the map
                    self.tile_map = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
    
    def handle_mouse_input(self) -> None:
        """Handle mouse input for placing/removing tiles."""
        mouse_pos = pg.mouse.get_pos()
        cell_size = self.screen_width // self.map_width
        grid_x = math.floor(mouse_pos[0] / cell_size)
        grid_y = math.floor(mouse_pos[1] / cell_size)
        
        # Ensure grid coordinates are within bounds
        if 0 <= grid_x < self.map_width and 0 <= grid_y < self.map_height:
            mouse_buttons = pg.mouse.get_pressed()
            
            if mouse_buttons[0]:  # Left click
                self.tile_map[grid_y][grid_x] = 1
            elif mouse_buttons[2]:  # Right click
                self.tile_map[grid_y][grid_x] = 0
                
        return grid_x, grid_y
    
    def draw(self, cursor_pos: Tuple[int, int]) -> None:
        """
        Draw the game state to the screen.
        
        Args:
            cursor_pos: Current position of the cursor in grid coordinates
        """
        # Fill background
        self.screen.fill((40, 40, 40))
        
        # Render the tile map
        map_surface = pg.Surface((self.map_width * self.tile_size, self.map_height * self.tile_size))
        self.autotile.render_map(map_surface, self.tile_map, self.show_masks)
        
        # Scale the map to fit the screen
        scaled_map = pg.transform.scale(
            map_surface, 
            (self.screen_width, self.screen_height)
        )
        self.screen.blit(scaled_map, (0, 0))
        
        # Draw cursor highlight
        cell_size = self.screen_width // self.map_width
        grid_x, grid_y = cursor_pos
        
        if 0 <= grid_x < self.map_width and 0 <= grid_y < self.map_height:
            cursor_color = (255, 255, 255) if self.tile_map[grid_y][grid_x] == 0 else (0, 255, 0)
            cursor_surface = pg.Surface((cell_size, cell_size), pg.SRCALPHA, 32)
            cursor_surface.fill(cursor_color + (100,))  # Add alpha value
            self.screen.blit(cursor_surface, (grid_x * cell_size, grid_y * cell_size))
        
        # Update display
        pg.display.flip()
    
    def run(self) -> None:
        """Run the main game loop."""
        while self.running:
            self.handle_events()
            cursor_pos = self.handle_mouse_input()
            self.draw(cursor_pos)
            self.clock.tick(60)  # Cap at 60 FPS
        
        pg.quit()


if __name__ == "__main__":
    game = Game(screen_size=(640, 640), map_size=(10, 10), tile_size=16)
    game.run()