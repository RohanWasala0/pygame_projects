from random import choice, randrange
from pygame import sprite, Vector2, Event, Rect, Color, Surface, SRCALPHA, draw, transform
from pygame import KEYDOWN, K_SPACE, event, USEREVENT
from typing import Dict, Optional, Any

class Environment(sprite.Sprite):
    """Manages the creation, rendering and movement of semi-transparent air that move across the screen."""
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                anchor: str = 'topleft',
                speed: float = 10.0,
                frames: list = [],
                debug: bool = False,
                ) -> None:
        """Initialize environment sprite

        Args:
            groups (sprite.Group): Pygame sprite group(s) that this belongs to 
            position (Optional[Vector2], optional): Starting position of this sprite. Defaults to None.
            anchor (str, optional): Position anchor point. Defaults to 'topleft'.
            speed (float, optional): Movement speed of the sprite Unit. Defaults to 10.0.
            frames (list, optional): List of air tile to create the sprite. Defaults to [].
            debug_box (bool, optional): Whether to draw a debug box around the sprite. Defaults to False.
        """
        super().__init__(groups)
        
        self.anchor: str = anchor
        self.group: sprite.Group = groups
        self.scale: float = randrange(2, 4)
        self.position: Vector2 = position or Vector2()
        self.velocity: Vector2 = Vector2(-1, 0) * speed

        self.AIR: Dict[str, Surface] = {
            '_01': frames[0],
            '_02': self.merge_surfaces(frames[1], frames[2]),
            '_03': self.merge_surfaces(frames[3], frames[4]),
            '_04': self.merge_surfaces(frames[5], frames[6]),
            '_05': self.merge_surfaces(frames[7], frames[8]),
            '_06': self.merge_surfaces(frames[9], frames[10]),
        }
        
        self.rect: Rect = None
        self.image: Surface = None
        self.render(debug)

    def update(self, deltaTime: float):
        self.kill() if self.position.x + self.image.width//2 < 0 else None
        
        self.position = self.position + (self.velocity * deltaTime)
        setattr(self.rect, self.anchor, self.position)
    
    def render(
        self,
        _debug_: bool = False,
    ):
        air_type = self.AIR[choice(list(self.AIR.keys()))].convert_alpha()
        scaled = transform.scale_by(air_type, self.scale)
        self.image = transform.flip(scaled, True, False)
        self.image.set_alpha(55)

        draw.rect(
            self.image, 
            Color('white'),
            self.image.get_rect(),
            width=1,
        ) if _debug_ else None

        self.image
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
    
    def merge_surfaces(
            self,
            surface1: Surface,
            surface2: Surface
    ) -> Surface:
        """Merges two surfaces horizontally by blit them on to a new surface

        Returns:
            Surface: The Merged surface
        """
        new_surface: Surface = Surface((surface1.width + surface2.width, surface1.height), SRCALPHA).convert_alpha()
        new_surface.set_colorkey(Color(0, 0, 0, 0))
        new_surface.blit(surface1, (0, 0))
        new_surface.blit(surface2, (surface1.width, 0))
        return new_surface

