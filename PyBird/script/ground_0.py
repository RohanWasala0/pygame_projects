from pygame import sprite, Surface, Vector2, Color, SRCALPHA, Rect, mask, Mask, transform, draw, BLEND_RGBA_MULT
from script.autotile import AutoTile, Tile
from random import choice
from typing import List, Tuple


class Ground(sprite.Sprite):
    def __init__(
            self,
            groups: sprite.Group,
            _mask: List[List[int]],
            _ground_tileset: Surface,
            _tile_mask: List[List[int]],
            height_width: Tuple[int, int],
            position: Vector2 = Vector2(),
            alpha: int = 255,
            speed: float = 45,
            scale: float = 1.0,
            anchor: str = 'topleft'
    ) -> None:
        """A Tile based ground obstacle that automatically generates connected tiles

        Args:
            groups (sprite.Group): Sprite group to which the object belongs 
            ground_tilemap (Surface): Source tileset surface
            tile_mask (List[List[int]]): 2D grid defining the tile presence in the tilset
            mask (List[List[int]]): 2D list defining a 3x3 connection mask for autotiling
            speed (float, optional): Speed of the obstacle
            scale (float, optional): Scale factor for a tile. Defaults to 1.0.
            position (Vector2, optional): Initial world position of the obstacle. Defaults to Vector2().
            anchor (str, optional): Attribute of the rect to aline the surface of the ground. Defaults to 'topleft'.
        """
        super().__init__(groups)
        self.group = groups
        self.alpha: int = alpha
        self.anchor: str = anchor
        self.scale: float = scale
        self.pass_check: bool = False
        self.height, self.width = height_width
        self.position: Vector2 = position or Vector2() 
        self.velocity: Vector2 = Vector2(-1, 0)* speed
        self.autotile: AutoTile = AutoTile(_ground_tileset, _tile_mask, _mask)

        self.render()
        self.mask: Mask = mask.from_surface(self.image)

    def _pregenerate_tile_map(
            self,
            height: int,
            width: int,
    ) -> List[List[int]]:
        """Generates a procedural tile map with a center platform shape
        Return: 
            The 2D grid of procedurally generated tilemap 
        """ 
        tile_map: List[List[int]] = [[0]* width for _ in range(height)]
        tile_map[0] = [0] * ((width - 3) // 2) + [1, 1, 1] + [0] * ((width - 3) // 2)
        center: int = width // 2
        left, right = center -1, center +1

        for y in range(height -1):
            for x in range(width):
                tile_map[y][x] = 1 if left <= x <= right else 0
            left = max(0, left - choice([0, 1]))
            right = min(width -1, right + choice([0, 1]))

        tile_map[height -1] = [1] * width
        return tile_map

    def _generate_ground(
            self,
            tile_map: List[List[int]],
    ) -> Surface:
        
        map_height = len(tile_map)
        map_width = len(tile_map[0]) if map_height>0 else 0
        tile_size = self.autotile.tile_size
        surface = Surface((map_width*tile_size.x, map_height*tile_size.y), SRCALPHA)
        surface.set_colorkey(Color('white'))
        surface.fill(Color('white'))

        for y, row in enumerate(tile_map):
            for x, cell in enumerate(row):
                if cell and x != len(row):
                    mask = self.autotile.generate_connectivity_mask(tile_map, Vector2(x, y), map_width, map_height)
                    tile: Tile = self.autotile.get_tile(mask) or self.autotile.tiles[0]
                    position = Vector2(tile_size.x* x, tile_size.y* y)
                    tile.draw(surface, position)

        return surface

    def _display_tiles(
            self
    ) -> Surface:
        """Displays a preview of all available tiles (for debugging).

        Returns:
            Surface: Surface of every single tile in the tilemap
        """
        column = 7
        tile_size = self.autotile.tile_size
        surface: Surface = Surface((tile_size.x* column, 
                                    tile_size.y* column))
        
        for idx, tile in enumerate(self.autotile.tiles):
            x = idx % column
            y = idx // column
            tile.draw(surface, Vector2(x* tile_size.x, y* tile_size.y))
        return surface
    
    def _reconnect_tiles(
            self,
            tile_map: List[List[int]]
    ) -> List[List[int]]:
        sprites = sorted(self.group.sprites(), key = lambda s: s.position.y)

        idx = sprites.index(self)
        new_tile_map = [[0] + row.copy() + [0] for row in tile_map]

        if idx > 0:
            left_sprite = sprites[idx -1]
            if hasattr(left_sprite, "tile_map"):
                left_map = left_sprite.tile_map
                temp = 0 
                if len(left_map) > len(self.tile_map):
                    temp = len(left_map) - len(self.tile_map)
                elif len(left_map) < len(self.tile_map):
                    temp = - len(self.tile_map) - len(left_map)
                for y in range(self.height):
                    # If the left sprite has a tile at the rightmost column, connect it to our leftmost column
                    u = y + temp if y + temp >= 0 else 0
                    if y < len(left_map) and left_map[u][-1] == 1:
                        new_tile_map[y][0] = 1

        # Check right neighbor
        if idx < len(sprites) - 1:
            right_sprite = sprites[idx + 1]
            if hasattr(right_sprite, "tile_map"):
                right_map = right_sprite.tile_map
                temp = 0 
                if len(right_map) > len(self.tile_map):
                    temp = len(right_map) - len(self.tile_map)
                elif len(right_map) < len(self.tile_map):
                    temp = -len(self.tile_map) - len(right_map)
                for y in range(self.height):
                    # If the right sprite has a tile at the leftmost column, connect it to our rightmost column
                    u = y + temp if y + temp >= 0 else 0
                    if y < len(right_map) and right_map[u][0] == 1:
                        new_tile_map[y][-1] = 1
        new_tile_map[self.height -1] = [1] * (self.width + 2)
        return new_tile_map

    
    def update(self, deltaTime: float):
        if self.position.x + self.image.width < 0: self.kill()

        self.position = self.position + (self.velocity * deltaTime)
        setattr(self.rect, self.anchor, self.position)
        self.mask = mask.from_surface(self.image)
    
    def render(self):
        tile_map = self._pregenerate_tile_map(self.height, self.width)
        tile_map = self._reconnect_tiles(tile_map)
        ground_surface: Surface = self._generate_ground(tile_map)
        # ground_surface: Surface = self._display_tiles()
        ground_surface = self.darken_surface(ground_surface, 0.8) if self.alpha < 255 else ground_surface

        self.image: Surface = Surface(ground_surface.size, SRCALPHA)
        self.image.blit(ground_surface)
        self.image = transform.scale_by(self.image, self.scale)
        
        # draw.circle(self.image, Color('red'), (0, 0), radius=3)
        # draw.rect(
        #     self.image,
        #     Color('white'),
        #     self.image.get_rect(),
        #     width= 1,
        # )
        
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
        
    def darken_surface(
        self,
        surface: Surface,
        factor: float,
    ) -> Surface:
        darkened_color = (factor * 255, factor * 255, factor * 255, 255)
        darkened: Surface = Surface(surface.size, SRCALPHA)
        surface.set_colorkey(darkened_color)
        darkened.fill(darkened_color)
        surface.blit(darkened, (0, 0), special_flags= BLEND_RGBA_MULT)
        return surface

    def check_score(
        self,
        bird_rect: Rect,
    ) -> int:
        if self.rect.left + 128 < bird_rect.left\
            and bird_rect.right < self.rect.right - 128\
                and self.pass_check == False:
                    self.pass_check = True
                    # print('inside')
        if self.pass_check == True:
            if bird_rect.left > self.rect.right - 128:    
                self.pass_check = False
                # print('outside')
                return 1
        return 0
