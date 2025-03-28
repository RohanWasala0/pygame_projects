import os
import pygame
import random

class TileMapGenerator:
    def __init__(self, frames):
        # Initialize Pygame
        pygame.init()
        
        # Screen setup
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Tile Map Generator")
        
        # Tile size (adjust based on your frame sizes)
        self.TILE_SIZE = 16
        
        # Ground tiles dictionary
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
        
        # Frames dictionary (placeholder)
        self.frames = frames
        
    def generate_tile_map(self, width=10, height=10):
        """
        Generate a 2D tile map with a pillar anchor as the starting point
        
        :param width: Width of the map in tiles
        :param height: Height of the map in tiles
        :return: 2D list representing the tile map
        """
        # Initialize the map with None
        tile_map = [[None for _ in range(width)] for _ in range(height)]
        
        # Place the anchor tile at the center of the map
        center_x = width // 2
        center_y = height - 3  # Place near the bottom
        
        # Place the anchor tile
        tile_map[center_y][center_x] = 'anchor'
        
        # Generate surrounding tiles based on the anchor's tile map
        anchor_tile_map = self.GROUND['anchor']['tile_map']
        
        # Offsets for surrounding tiles
        offsets = [
            (-1, 1, 'corner_left'),   # Bottom left corner
            (0, 1, 'dirt'),            # Bottom center dirt
            (1, 1, 'corner_right'),   # Bottom right corner
            (-1, 0, 'stright_left'),  # Left side straight
            (1, 0, 'stright_right')   # Right side straight
        ]
        
        # Place surrounding tiles
        for dx, dy, tile_type in offsets:
            nx, ny = center_x + dx, center_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                tile_map[ny][nx] = tile_type
        
        return tile_map
    
    def render_tile_map(self, tile_map):
        """
        Render the tile map on the screen
        
        :param tile_map: 2D list of tile types
        """
        # Clear the screen
        self.screen.fill((0, 0, 0))
        
        # Render tiles
        for y, row in enumerate(tile_map):
            for x, tile_type in enumerate(row):
                if tile_type:
                    # Select appropriate frame based on tile type
                    if tile_type == 'anchor':
                        frame = self.GROUND['anchor']['frame']
                    elif tile_type == 'corner_left':
                        frame = self.GROUND['corner']['left']['frame']
                    elif tile_type == 'corner_right':
                        frame = self.GROUND['corner']['right']['frame']
                    elif tile_type == 'stright_left':
                        frame = self.GROUND['stright']['left']['frame'][0]
                    elif tile_type == 'stright_right':
                        frame = self.GROUND['stright']['right']['frame'][0]
                    elif tile_type == 'dirt':
                        frame = self.GROUND['dirt']['frame'][0]
                    else:
                        continue
                    
                    # Render the frame
                    self.screen.blit(frame, (x * self.TILE_SIZE, y * self.TILE_SIZE))
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """
        Main game loop
        """
        # Generate the tile map
        tile_map = self.generate_tile_map()
        
        # Render the tile map
        self.render_tile_map(tile_map)
        
        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
        
        # Quit Pygame
        pygame.quit()

# Example usage (you'll need to provide the actual frames)
def main():
    # Placeholder for frames - replace with your actual frame surfaces
    frames = []
    for entry in os.scandir('./PyBird/assets/Retro-Lines-16x16/ground_tiles'):
        frames.append(pygame.image.load(entry.path))
    
    # Create generator and run
    generator = TileMapGenerator(frames)
    generator.run()

if __name__ == "__main__":
    main()