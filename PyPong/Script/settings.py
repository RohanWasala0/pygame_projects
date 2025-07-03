from pygame import (
        sprite, 
        Vector2, 
        draw, 
        Color, 
        Surface, 
        Rect, 
        display,
        transform,
        SRCALPHA,
        mask,
        KEYDOWN,
        FINGERUP,
        FINGERDOWN,
        K_w, K_s, K_UP, K_DOWN, K_a, K_d, K_LEFT, K_RIGHT,
    ) 
from typing import Tuple, Optional

from utils import FONT_PATH, keyboard_keys, FONT_PATH_04b, logo
from PyGextras import TextCanvas
from PyGextras import InputManager

class Settings(sprite.Sprite):
    def __init__(
        self, 
        groups: sprite.Group = {},
        anchor: str = 'topleft',
        color: Color = Color('black'),
        position: Optional[Vector2] = Vector2(), 
        dimensions: Tuple[int, int] = (0, 0), 
    ):
        super().__init__(groups)
        
        self.color = color
        self.group = groups
        self.anchor = anchor
        self.position = position 
        self.dimensions = dimensions
        self.touched = False

        self.input_manager = InputManager()
        self.input_manager.input_chart = {
            'discrete': {
                KEYDOWN: {
                    (K_UP, K_w): self.move_up,
                    (K_s, K_DOWN): self.move_down,
                    (K_a, K_LEFT): self.move_left,
                    (K_d, K_RIGHT): self.move_right,
                }
            },
            'touch': {
                FINGERDOWN: {}
            }
        }
        self.canvas_group = sprite.Group()
        self.controls_scene = sprite.Group()
        self._initialize_text()
        print(self.input_manager.input_chart)
        self.list_of_options = [self.play_text, self.controls_text, self.touch_controls_text, self.quit]
        self.playable_types = [self.single_player, self.two_player]
        self.current_selection = self.play_text
        self.pressed_play = False

        self.image = Surface(self.dimensions, SRCALPHA) if self.dimensions != (0, 0) else Surface((5, 5), SRCALPHA)
        self.render()

    def update(self, deltaTime: float):
        self.canvas_group.update(deltaTime)
        self.render()

    def render(self):
        self.image.fill(Color(0,0,0,0))
        self.image.set_colorkey(Color('black'))
        self.image.fill(Color('black'))
        self.image.fill(self.color)

        # self.debug(40, self.image)
        self.canvas_group.draw(self.image)
        self.image.blit(
            transform.scale(keyboard_keys[0], (38, 38)),
            (32*5, 64+32+32+5)
        ) if self.current_selection == self.play_text else None
        self.image.blit(
            transform.scale(keyboard_keys[1], (38, 38)),
            (32*5 + 32, 64+32+32+5)
        ) if self.current_selection == self.play_text else None

        self.image.blit(
            transform.scale(keyboard_keys[0], (38, 38)),
            (32*9, 64+32+32+32+16+5)
        ) if self.current_selection == self.controls_text else None
        self.image.blit(
            transform.scale(keyboard_keys[1], (38, 38)),
            (32*9 + 32, 64+32+32+32+16+5)
        ) if self.current_selection == self.controls_text else None

        self.image.blit(
            transform.scale(keyboard_keys[0], (38, 38)),
            (32*9, 64+32+32+32+16+5)
        ) if self.current_selection == self.controls_text else None
        self.image.blit(
            transform.scale(keyboard_keys[1], (38, 38)),
            (32*9 + 32, 64+32+32+32+16+5)
        ) if self.current_selection == self.controls_text else None

        self.image.blit(
            transform.scale(keyboard_keys[0], (38, 38)),
            (32*11+16, 7*32)
        ) if self.current_selection == self.touch_controls_text else None
        self.image.blit(
            transform.scale(keyboard_keys[1], (38, 38)),
            (32*11+16 + 32, 7*32)
        ) if self.current_selection == self.touch_controls_text else None

        self.image.blit(
            transform.scale(keyboard_keys[0], (38, 38)),
            (32*5, 8*32+13)
        ) if self.current_selection == self.quit else None
        self.image.blit(
            transform.scale(keyboard_keys[1], (38, 38)),
            (32*5 + 32, 8*32+13)
        ) if self.current_selection == self.quit else None

        self.image.blit(
            transform.scale(keyboard_keys[2], (32, 32)),
            (10*16, 8*16)
        ) if self.current_selection == self.single_player else None
        self.image.blit(
            transform.scale(keyboard_keys[3], (32, 32)),
            (10*16 + 35, 8*16)
        ) if self.current_selection == self.single_player else None

        self.image.blit(
            transform.scale(keyboard_keys[0], (32, 32)),
            (22*16, 8*16)
        ) if self.current_selection == self.two_player else None
        self.image.blit(
            transform.scale(keyboard_keys[1], (32, 32)),
            (22*16 +35, 8*16)
        ) if self.current_selection == self.two_player else None

        self.image.blit(
            transform.scale(logo, (logo.get_width()/2.75, logo.get_height()/2.75)),
            (7*40, 8*40)
        )


        self.rect: Rect = self.image.get_rect()
        self.mask: mask.Mask = mask.from_surface(self.image)
        setattr(self.rect, self.anchor, self.position)

    def _initialize_text(self,) -> None:
        self.music_text = TextCanvas(
            raw= f"[position: 32, 32][text: PyPong][align: center][effect: shadow]",
            groups= self.canvas_group,
            font_path= FONT_PATH,
            font_size= 64
        )
        self.play_text = TextCanvas(
            raw=f"[position: 32, 64 + 32 + 32][text: PLAY][align: center][effect: shadow, sin_letter]",
            groups= self.canvas_group,
            font_path= FONT_PATH,
            font_size= 32
        )
        self.single_player = TextCanvas(
            raw=f"[position: 32, 4*32][text: 1 Player][effect: shadow, sin_letter]",
            # groups= self.canvas_group,
            font_path= FONT_PATH,
            font_size= 16
        )
        self.two_player = TextCanvas(
            raw=f"[position: 32*7, 4*32][text: 2 Player]",
            # groups= self.canvas_group,
            font_path= FONT_PATH,
            font_size= 16
        )
        self.controls_text = TextCanvas(
            raw=f"[position: 32, (64+32+32)+32+16][text: CONTROLS][align: center]",
            groups= self.canvas_group,
            font_path= FONT_PATH,
            font_size= 32
        )
        self.touch_controls_text = TextCanvas(
            raw=f"[position: 32, 7*32][text: TOUCH CONTROLS][align: center]",
            groups= self.canvas_group,
            font_path= FONT_PATH,
            font_size= 24
        )
        self.quit = TextCanvas(
            raw= f"[position: 32, 8*32+8][text: QUIT][align: center]",
            groups= self.canvas_group,
            font_path= FONT_PATH,
            font_size= 32
        )
        self.add_touch_controls((self.play_text, self.controls_text, self.touch_controls_text, self.quit))

    def debug(self, spacing, grid_surface):
        draw.rect(
            grid_surface,
            Color('white'),
            grid_surface.get_rect(),
            width= 1,
        )

        width, height = self.dimensions
        grid_color = Color('white')
        for x in range(0, width, spacing):
            draw.line(grid_surface, grid_color, (x, 0), (x, height)) 
        for y in range(0, height, spacing):
            draw.line(grid_surface, grid_color, (0, y), (width, y)) 

    def move_up(self):
        if self.pressed_play:
            self.pressed_play = False
            self.canvas_group.add(self.play_text)
            self.play_text.effects_list = []
            self.canvas_group.remove(self.single_player)
            self.canvas_group.remove(self.two_player)
            selection = self.list_of_options[-1]
            selection.effects_list = ['shadow','sin_letter']
            self.current_selection = selection        
        else:
            index = self.list_of_options.index(self.current_selection)
            self.current_selection.effects_list = []
            index -= 1
            selection = self.list_of_options[index] if not index < 0 else self.list_of_options[len(self.list_of_options)-1]
            selection.effects_list = ['shadow','sin_letter']
            self.current_selection = selection        
    def move_down(self):
        if self.pressed_play:
            self.pressed_play = False
            self.canvas_group.add(self.play_text)
            self.play_text.effects_list = []
            self.canvas_group.remove(self.single_player)
            self.canvas_group.remove(self.two_player)
            selection = self.list_of_options[1]
            selection.effects_list = ['shadow','sin_letter']
            self.current_selection = selection        
        else:
            index = self.list_of_options.index(self.current_selection)
            self.current_selection.effects_list = []
            index += 1
            self.current_selection = self.list_of_options[index] if index < len(self.list_of_options) else self.list_of_options[0]
            self.current_selection.effects_list = ['shadow','sin_letter']

    def move_left(self):
        if self.pressed_play:
            index = self.playable_types.index(self.current_selection)
            self.current_selection.effects_list = []
            index -= 1
            selection = self.playable_types[index] if not index < 0 else self.playable_types[len(self.playable_types)-1]
            selection.effects_list = ['shadow','sin_letter']
            self.current_selection = selection        
    def move_right(self):
        if self.pressed_play:
            index = self.playable_types.index(self.current_selection)
            self.current_selection.effects_list = []
            index += 1
            self.current_selection = self.playable_types[index] if index < len(self.playable_types) else self.playable_types[0]
            self.current_selection.effects_list = ['shadow','sin_letter']
    def move_to_selected(self, selected):
        print(selected.text)
        # if self.pressed_play:
        #     self.add_touch_controls((self.play,))
        self.current_selection.effects_list = []
        self.current_selection: TextCanvas = selected
        self.current_selection.effects_list = ['shadow', 'sin_letter']
        self.touched = True

    def change_scene(self, scene: sprite.Group):
        print("scene changed")

    def add_touch_controls(self, list_of_controls):
        for i, x in enumerate(list_of_controls):
            # print(x.position)
            x1 = round(x.rect.x / self.dimensions[0], 4)
            x2 = round((x.rect.x + x.image.get_width())/self.dimensions[0], 4)
            y1 = round(x.rect.y/self.dimensions[1], 4)
            y2 = round((x.rect.y + x.image.get_height())/self.dimensions[1], 4)
            def create_touch_handler(target_canvas):
                return lambda event: self.move_to_selected(target_canvas)
            
            self.input_manager.input_chart['touch'][FINGERDOWN][(x1, x2, y1, y2)] = create_touch_handler(x)