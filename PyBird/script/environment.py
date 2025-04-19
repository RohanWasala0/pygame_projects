from random import choice, randrange
from pygame import sprite, Vector2, Event, Rect, Color, Surface, SRCALPHA, draw, transform
from pygame import KEYDOWN, K_SPACE, event, USEREVENT
from typing import Dict, Optional, Any

class Environment(sprite.Sprite):
    """Mangaes the creation, rendering and movement of semi-transparent air
       that move across the screen.
    """
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                anchor: str = 'topleft',
                speed: float = 10.0,
                frames: list = [],
                debug_box: bool = False,
                ) -> None:
        """Initialize environment sprite

        Args:
            groups (sprite.Group): Pygame sprite group(s) that this belongs to 
            position (Optional[Vector2], optional): Starting position of this sprite. Defaults to None.
            anchor (str, optional): Position anchor point. Defaults to 'topleft'.
            speed (float, optional): Movement speed of the sprite Unit. Defaults to 10.0.
            frames (list, optional): List of air tile to create the spirte. Defaults to [].
            debug_box (bool, optional): Wheather to draw a debug box around the sprite. Defaults to False.
        """
        super().__init__(groups)
         
        self.group: sprite.Group = groups
        self.position: Vector2 = position or Vector2()
        self.anchor: str = anchor 
        self.debug_box: bool = debug_box
        self.scale: float = randrange(2, 4)
        self.velocity: Vector2 = Vector2(-1, 0) * speed

        self.input_chart: Dict[Event, Any] = {}

        self.AIR: Dict[str, Surface] = {
            '_01': frames[0],
            '_02': self.merge_surfaces(frames[1], frames[2]),
            '_03': self.merge_surfaces(frames[3], frames[4]),
            '_04': self.merge_surfaces(frames[5], frames[6]),
            '_05': self.merge_surfaces(frames[7], frames[8]),
            '_06': self.merge_surfaces(frames[9], frames[10]),
        }
        
        self.image: Surface = Surface((0, 0), SRCALPHA)
        self.image.set_colorkey(Color(0, 0, 0, 0))
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)

        self.render()
    
    def handling_input(self, event: Event) -> None:

        if event.type not in self.input_chart:
            return
        handler = self.input_chart[event.type]
        try:
            if callable(handler): handler()
            else:
                # print(self.get_class_properties(event))
                for name in dir(event):
                    if not callable(getattr(event, name)) and not name.startswith("__") and not isinstance(getattr(event, name), dict):
                        if getattr(event, name) in self.input_chart[event.type]:
                            action = self.input_chart[event.type][getattr(event, name)] 
                            if action: action()

        # if event_type_action := self.input_chart.get(event.type):
        #     action = event_type_action if callable(event_type_action) else event_type_action.get(getattr(event, 'key', None)) or \
        #              event_type_action.get(getattr(event, 'ui_element', None)) 
            
        #     if action:
        #         try:
        #             action()
        except Exception as e:
            print(f"Error executing the action:{handler} with error:{e}")

    def update(self, deltaTime: float):
        self.kill() if self.position.x + self.image.width//2 < 0 else None
        
        position = self.position + (self.velocity * deltaTime)
        self.position = Vector2.lerp(position, self.position, deltaTime)
        setattr(self.rect, self.anchor, self.position)
    
    def render(self):
        air_type = self.AIR[choice(list(self.AIR.keys()))].convert_alpha()
        size = tuple(x*self.scale for x in air_type.size) 
        scaled = transform.scale(air_type, size)
        self.image = transform.flip(scaled, True, False)
        self.image.set_alpha(55)

        draw.rect(
            self.image, 
            Color('white'),
            self.image.get_rect(),
            width=1,
        ) if self.debug_box else None

        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
    
    def merge_surfaces(
            self,
            surface1: Surface,
            surface2: Surface
    ) -> Surface:
        """Merges two surfaces horizontally by blit them on to a new surface

        Args:
            surface1 (Surface): Surface that goes first
            surface2 (Surface): Surface that goes after first

        Returns:
            Surface: The Merged surface
        """
        new_surface: Surface = Surface((surface1.width + surface2.width, surface1.height), SRCALPHA).convert_alpha()
        new_surface.set_colorkey(Color(0, 0, 0, 0))
        new_surface.blit(surface1, (0, 0))
        new_surface.blit(surface2, (surface1.width, 0))
        return new_surface

    def get_class_properties(self, obj_or_cls):
        return {
            name: getattr(obj_or_cls, name)
            for name in dir(obj_or_cls)
            if not callable(getattr(obj_or_cls, name)) and not name.startswith("__")
        }
