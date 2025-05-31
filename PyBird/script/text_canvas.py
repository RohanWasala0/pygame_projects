from pygame import KEYDOWN, K_SPACE, SRCALPHA
from pygame import sprite, Vector2, draw, Color, Surface, Rect, event, font
from typing import Tuple, Optional, Dict, List
import pygame.freetype as ft
import math

class text_canvas(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                font_size: int = 10,                
                font_path: str = None,
                position: Optional[Vector2] = Vector2(), 
                anchor: str = 'topleft',
                color: Color = Color('white'),
                background_color: Color = Color('black'),
                text: str = 'Testing',
                ) -> None:
        super().__init__(groups)
        
        self.time = 0
        self.text = text
        self.color = color
        self.anchor = anchor
        self.padding = 4
        self.border_width = 4
        self.margin = 2
        self.position = position or Vector2(0, 0)
        self.initial_position = self.position
        self.width, self.height = 0, 0
        self.background_color = background_color
        self.align = 'center'

        # self.font:font.Font = font.Font(font_path, font_size) 
        # self.font.align = align
        
        self.ft_font: ft.Font = ft.Font(font_path, font_size)
        self.ft_font.pad = False
        self.ft_font.antialiased = False
        
        self.render()
    
    def update(self, deltaTime: float):
        self.render()

    def render(self):
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        self.list_surfaceText = self.generate_content()
        canvas_size = self.calculate_size(self.list_surfaceText)
        position_list = self.calculate_position(self.list_surfaceText)
        
        self.image = Surface(canvas_size)
        self.image.fill(self.background_color)
        self.image.set_colorkey(Color('black'))
        
        if len(self.list_surfaceText) == len(position_list):
            for line, position in zip(self.list_surfaceText, position_list):
                rect = line.get_rect(center = (self.image.width//2, position[1] + line.height//2))
                # rect = line.get_rect(topleft = position)
                # rect = line.get_rect(topright = (self.image.width - position[0], position[1]))
                self.image.blit(line, rect) 
        
        # draw.rect(
        #     self.image,
        #     Color('white'),
        #     self.image.get_rect(),
        #     width= 1,
        #     border_radius= 1,
        # )

        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)

    def calculate_size(self, surface_list: List[Surface]) -> Tuple[int, int]:
        width = max(line.width for line in surface_list) if surface_list else 0
        width = width + 2*self.margin + 2*self.border_width + 2*self.padding
        # height = sum(line.height for line in surface_list) if surface_list else 0
        
        height = 2*self.margin + self.border_width
        for line in surface_list:
            height += self.border_width + 2*self.padding + line.height
        
        return width, height

    def generate_content(
        self
    ) -> List[Surface]:
        surface_list: List[Surface] = []
        lines = self.text.split('\n')
        for line in lines: 
            text_surf, text_rect = self.ft_font.render(
                text= line,
                fgcolor= self.color,
                bgcolor= self.background_color,
            )
            # draw.rect(
            #     text_surf,
            #     Color('white'),
            #     text_surf.get_rect(),
            #     width= 1
            # )
            surface_list.append(text_surf)
        return surface_list

    def calculate_position(
        self,
        surface_list: List[Surface]
    ) -> List[Tuple[int, int]]:
        position_list = []
        x = self.border_width + self.padding + self.margin
        y = self.margin + self.border_width + self.padding
        for line in surface_list:
            position_list.append((x, y))
            y += line.height + 2*self.padding + self.border_width
        return position_list

    def sinusoidal_motion(self, deltaTime: float, amplitude: int, frequency: float, speed: int) -> None:
        self.time += deltaTime * speed
        sine = amplitude * math.sin(frequency * self.time)
        self.position = Vector2(self.position.x, self.initial_position.y + sine)