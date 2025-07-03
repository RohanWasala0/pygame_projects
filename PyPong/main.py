import sys, platform
import asyncio
import pygame
import random
import math
from functools import wraps
from enum import Enum, auto

from PyGextras  import TextCanvas as tc
from PyGextras import InputManager
from utils import *
from Script.ball import Ball
from Script.paddle import Paddle
from Script.settings import Settings

if sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"

class GameState(Enum):
    Menu = auto()
    TOUCH_CONTROLS = auto()
    KEYBOARD_CONTROLS = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()

# decorators
def debug(
    width: int,
    height: int,
    grid_color: pygame.Color = pygame.Color(173, 170, 170, 75),
    spacing: int = 40
):
    def decorator(render):
        @wraps(render)
        def wrapper(self, *args, **kwargs):
            grid_surface: pygame.Surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
            
            for x in range(0, width, spacing):
                pygame.draw.line(grid_surface, grid_color, (x, 0), (x, height)) 
            for y in range(0, height, spacing):
                pygame.draw.line(grid_surface, grid_color, (0, y), (width, y)) 

            kwargs['debug_surface'] = grid_surface
            return render(self, *args, **kwargs)
            # return result
        return wrapper
    return decorator

class PyPong():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("PyPong")

        print("started")
        self.state = GameState.Menu
        self.display = pygame.display.set_mode(SCREEN_SIZE, pygame.SRCALPHA)
        self.screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.screen_group = pygame.sprite.Group()
        self.screen_input_manager = InputManager()

        self.player1_score = 0
        self.player2_score = 0
        self.time = 0
        self.ai = False
        self.ai_dead_zone = 40

        self.hit = pygame.mixer.Sound(HIT)
        self.point = pygame.mixer.Sound(POINT)

        self._initialize_text_canvas()
        self._initialize_objects()
        [print(f"{x}") for x in self.screen_group.spritedict]
        print((keyboard_keys[-1].width*4, keyboard_keys[-1].height*4))

        self.screen_input_manager.input_chart = {
            'discrete': {
                pygame.QUIT: self.quit,
                pygame.K_ESCAPE: self.change_to_menu,
                pygame.KEYDOWN: {pygame.K_r: self.reset_game},
            },
            'touch': {
                pygame.FINGERUP:{
                    (0.25, 0.375, 0.0, 0.125): lambda event: self.reset_game(),
                    (0.625, 0.75, 0.0, 0.125): lambda event: self.change_to_menu(),
                }
            },
        }

    def _initialize_objects(self) -> None:
        self.ball = Ball(
            groups= self.screen_group,
            anchor= 'center',
            position= pygame.Vector2(WIDTH//2, HEIGHT//2),
            radius= 10 ,
            color= BALL_GREY,
        )

        self.player1 = Paddle(
            groups= self.screen_group,
            keys= (pygame.K_w, pygame.K_s),
            zone= (0.0, 0.25, 0.0, 1.0),
            anchor= 'center',
            position= pygame.Vector2(60, HEIGHT//2),
            dimensions= (40, 150),
            color= PADDLE_BROWN,
        )
        self.player2 = Paddle(
            groups= self.screen_group,
            keys= (pygame.K_UP, pygame.K_DOWN),
            zone= (0.75, 1.0, 0.0, 1.0),
            anchor= 'center',
            position= pygame.Vector2(WIDTH - 60, HEIGHT//2),
            dimensions= (40, 150),
            color= PADDLE_BROWN,
        )
        self.menu_group = pygame.sprite.Group()
        self.settings_menu = Settings(
            groups= self.menu_group,
            anchor= 'center',
            position= pygame.Vector2(WIDTH//2, HEIGHT//2),
            dimensions= (WIDTH-(40*4), HEIGHT-(40*2)),
            color= PADDLE_BROWN,
        )
        self.settings_menu.input_manager.input_chart['discrete'][pygame.KEYDOWN].update({pygame.K_SPACE: self.select_in_menu})

    def _initialize_text_canvas(self) -> None:

        self.score = tc(
            raw= f"[position: {WIDTH}//2, 60][color: white][align: center][text: {self.player2_score}-{self.player1_score}]",
            font_path= FONT_PATH,
            font_size= 25,
            groups= self.screen_group,
            anchor= 'center'
        )
        # self.reset_text = tc(
        #     raw= f"[position: 20, 20][size: 15][align: left][color: white][text: 'r'\nto reset]",
        #     font_path= font_path,
        #     groups= self.screen_group,
        # )

    def animated_background(self, spacing, time) -> None:
        time = time % spacing
        grid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for index, color in enumerate((PADDLE_BROWN, BALL_GREY, PARTICLES_BEIGE)):
            for i in range(0, WIDTH, spacing): #vertical lines
                x = i + time + (index*8)
                pygame.draw.line(grid_surface, color, (x, 0), (x, HEIGHT))
            for j in range(0, HEIGHT, spacing):
                y = j + time + (index*8)
                pygame.draw.line(grid_surface, color, (0, y), (WIDTH, y))
        grid_surface.set_alpha(60)
        return grid_surface

    @debug(WIDTH, HEIGHT)
    def render(
        self,
        debug_surface:pygame.Surface = None,
    ) -> None:
        self.screen.fill(BACKGROUND_BLACK)
        self.screen.blit(debug_surface, (0, 0)) if debug_surface else None
        animated_texture = self.animated_background(40, self.time)
        self.screen.blit(animated_texture, (0, 0)) if not debug_surface else None

        self.dotted_line(self.screen)
        self.screen.blit(pygame.transform.scale(keyboard_keys[-1], (keyboard_keys[-1].width*4, keyboard_keys[-1].height*4)), (4*40, 0))
        self.screen.blit(pygame.transform.scale(keyboard_keys[-3], (keyboard_keys[-3].width*4, keyboard_keys[-3].height*4)), keyboard_keys[-3].get_rect(topright=(WIDTH-5*40, 0)))

        self.ball.draw_trail(self.screen)
        self.screen_group.draw(self.screen)
        self.screen = self.blur(self.screen) if self.state == GameState.Menu else self.screen
        # self.screen_group.add(self.settings_menu)
        self.menu_group.draw(self.screen) 

        self.display.blit(self.screen)

    def handle_input(self) -> None:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        self.screen_input_manager.handle_input(events, keys)
        if self.state == GameState.PLAYING:
            self.ball.input_manager.handle_input(events, keys)
            self.player1.input_manager.handle_input(events, keys)
            self.player2.input_manager.handle_input(events, keys) if self.ai == False else None
        elif self.state == GameState.Menu:
            self.settings_menu.input_manager.handle_input(events, keys)

        self.select_in_menu() if self.settings_menu.touched else None

    def update(self, deltaTime: float) -> None:

        self.time += 40 * deltaTime
        self.move_ai(deltaTime)
        self.screen_group.update(deltaTime)
        self.menu_group.update(deltaTime) 
        self.paddle_collision()
        self.point_scored()

    def paddle_collision(self) -> None:

        def handle_collision(paddle, direction, angle_range):
            angles = [angle + random.randint(-10, 10) for angle in angle_range]

            self.ball.velocity = self.ball.change_angle(angles)

        if self.player1.rect.colliderect(self.ball.rect):
            handle_collision(self.player1, -1, [315, 405]) if self.ball.position.x > 63 else None
            self.ball.speed += 50
            self.hit.play()
        elif self.player2.rect.colliderect(self.ball.rect):
            handle_collision(self.player2, 1, [135, 225]) if self.ball.position.x < WIDTH-63 else None
            self.ball.speed += 50
            self.hit.play()

    def point_scored(self) -> None:
        if self.ball.position.x < self.ball.radius:
            self.player1_score += 1
            self.ball.reset()
            self.point.play()
        elif self.ball.position.x > WIDTH - self.ball.radius:
            self.player2_score += 1
            self.ball.reset()
            self.point.play()
        self.score.text = f"{self.player2_score}-{self.player1_score}"

    def reset_game(self):
        self.ball.reset()
        self.player1.reset()
        self.player2.reset()
        self.player1_score, self.player2_score = 0, 0
        self.ai = False

    def dotted_line(self, surface:pygame.Surface):
        x1, y1 = pygame.Vector2(WIDTH//2, 0)
        x2, y2 = pygame.Vector2(WIDTH//2, HEIGHT)

        dist = math.hypot(x2-x1, y2-y1)
        dx, dy = (x2 - x1)/dist, (y2-y1)/dist
        for i in range(0, int(dist), 10):
            start_pos = x1 + dx*i, y1 + dy*i
            end_pos = x1 + dx*(i+5), y1 + dy*(i+5)
            pygame.draw.line(surface, pygame.Color('white'), start_pos, end_pos)

    def quit(self):
        print('Shutting Down')
        pygame.quit()
        sys.exit()

    def blur(self, surface: pygame.Surface, factor: float = 0.25) -> pygame.Surface:
        if not (0 < factor < 1):
            raise ValueError("factor should in between 0 - 1")

        small_size = (max(1, int(surface.width * factor)),max(1, int(surface.height * factor)))
        
        small = pygame.transform.smoothscale(surface, small_size)
        result = pygame.transform.smoothscale(small, surface.get_size())
        return result

    def change_scene(self):
        print("changing scene")
        self.state = GameState.PLAYING
        self.menu_group.empty()

    def easeOut(self, point_a: pygame.Vector2, point_b: pygame.Vector2, speed: int, deltaTime: float):
        direction = point_b - point_a
        distance = direction.length()

        progress = min(speed* deltaTime/distance, 1.0)
        ease_progress = math.sin((progress*math.pi)/2) 
        return point_a + direction*ease_progress

    def select_in_menu(self):
        match self.settings_menu.current_selection:
            case self.settings_menu.play_text:
                # self.change_scene()
                self.settings_menu.current_selection = self.settings_menu.single_player
                self.settings_menu.canvas_group.remove(self.settings_menu.play_text)
                self.settings_menu.canvas_group.add(self.settings_menu.single_player)
                self.settings_menu.canvas_group.add(self.settings_menu.two_player)
                self.settings_menu.pressed_play = True
                del self.settings_menu.input_manager.input_chart['touch'][pygame.FINGERDOWN][(0.0667, 0.3333, 0.32, 0.425)]
                self.settings_menu.add_touch_controls((self.settings_menu.single_player, self.settings_menu.two_player))
            case self.settings_menu.controls_text:
                self.menu_group.empty()
                self.state = GameState.KEYBOARD_CONTROLS
                self.screen_group.add(self.keyboard_controls())
            case self.settings_menu.touch_controls_text:
                self.menu_group.empty()
                self.state = GameState.TOUCH_CONTROLS
                self.screen_group.add(self.touch_controls())
            case self.settings_menu.quit:
                self.quit()
            case self.settings_menu.single_player:
                self.ai = True
                self.change_scene()
            case self.settings_menu.two_player:
                self.ai = False
                self.change_scene()
        self.settings_menu.touched = False
        # if self.settings_menu.pressed_play:
        #     self.settings_menu.add_touch_controls()

    def change_to_menu(self):
        if self.state == GameState.TOUCH_CONTROLS:
            self.state = GameState.Menu
            self.menu_group.add(self.settings_menu)
            for x in self.screen_group.sprites():
                if hasattr(x, 'tag') and  x.tag == 'touch controls':
                    self.screen_group.remove(x)
            self.screen_group.remove(list(self.screen_group.spritedict.keys())[-1])
        elif self.state == GameState.KEYBOARD_CONTROLS:
            self.state = GameState.Menu
            self.menu_group.add(self.settings_menu)
            for x in self.screen_group.sprites():
                if hasattr(x, 'tag') and  x.tag == 'keyboard controls':
                    self.screen_group.remove(x)
            self.screen_group.remove(list(self.screen_group.spritedict.keys())[-1])
        elif self.state == GameState.PLAYING:
            self.reset_game()
            self.state = GameState.Menu
            self.settings_menu.current_selection = self.settings_menu.play_text
            self.menu_group.add(self.settings_menu)

    def touch_controls(self):
        touch = pygame.sprite.Sprite()
        touch.image = pygame.Surface(self.screen.size, pygame.SRCALPHA)
        pygame.draw.rect(
            touch.image,
            pygame.Color('white'),
            pygame.Rect((0, 0), (WIDTH*0.25, HEIGHT)),
            5
        )
        pygame.draw.rect(
            touch.image,
            pygame.Color('white'),
            pygame.Rect((0.75*WIDTH, 0), (WIDTH*0.25, HEIGHT)),
            5
        )
        pygame.draw.rect(
            touch.image,
            pygame.Color('white'),
            pygame.Rect((WIDTH*0.25, HEIGHT*0.25), (WIDTH*0.5, WIDTH*0.5)),
            5
        )
        tc(
            groups= self.screen_group,
            raw= f"[text: Player1][position: 40, 40*9]",
            font_path= FONT_PATH,
            font_size= 15,
            tag= 'touch controls'
        )
        tc(
            groups= self.screen_group,
            raw= f"[text: Player2][position: 15*40, 40*9]",
            font_path= FONT_PATH,
            font_size= 15,
            anchor= 'topright',
            tag= 'touch controls'
        )
        tc(
            groups= self.screen_group,
            raw= f"[text: Touch to\nPLAY][position: 8*40, 40*7]",
            font_path= FONT_PATH,
            font_size= 15,
            anchor= "center",
            tag= 'touch controls'
        )
        touch.rect = touch.image.get_rect()
        return touch

    def keyboard_controls(self):
        _keyboard = pygame.sprite.Sprite()
        _keyboard.image = pygame.Surface(self.screen.size, pygame.SRCALPHA)

        _keyboard.image.blit(pygame.transform.scale(keyboard_keys[38], (42, 42)), (40, 40*9))
        _keyboard.image.blit(pygame.transform.scale(keyboard_keys[34], (42, 42)), (40, 40*9 + 42))
        _keyboard.image.blit(pygame.transform.scale(keyboard_keys[-2], (42, 42)), (2, 40*9 + 42))
        _keyboard.image.blit(pygame.transform.scale(keyboard_keys[-2], (42, 42)), (82, 40*9 + 42))

        _keyboard.image.blit(pygame.transform.scale(keyboard_keys[0], (42, 42)), (14*40, 40*9))
        _keyboard.image.blit(pygame.transform.scale(keyboard_keys[1], (42, 42)), (14*40, 40*9 + 42))
        _keyboard.image.blit(pygame.transform.scale(keyboard_keys[-2], (42, 42)), (14*40 - 42, 40*9 + 42))
        _keyboard.image.blit(pygame.transform.scale(keyboard_keys[-2], (42, 42)), (14*40 + 42, 40*9 + 42))

        _keyboard.image.blit(pygame.transform.scale(space_key, (space_key.width*3, 42)), (6*40 - 20, 40*9))
        tc(
            f"[text: To Play][position: 9*40 + 20, 40*9 + 20]",
            self.screen_group, FONT_PATH, 15, 'keyboard controls', 'center')

        _keyboard.image.blit(pygame.transform.scale(keyboard_keys[33], (42, 42)), (40, 0))
        tc(
            f"[text: To Reset][position: 2*40, 10]",
            self.screen_group, FONT_PATH, 15, 'keyboard controls')

        _keyboard.image.blit(pygame.transform.scale(escape_key, (escape_key.width*3, 42)), (14*40 - 20, 0))
        tc(
            f"[text: To Menu][position: 11*40 - 10, 10]",
            self.screen_group, FONT_PATH, 15, 'keyboard controls')

        _keyboard.rect = _keyboard.image.get_rect()
        return _keyboard

    def move_ai(self, deltaTime: float):
        x_player2 = self.player2.axis_smoothing(self.player2.direction.x, self.player2.target_direction.x, deltaTime)
        y_player2 = self.player2.axis_smoothing(self.player2.direction.y, self.player2.target_direction.y, deltaTime) 

        if abs(self.ball.position.y - self.player2.position.y) > self.ai_dead_zone:
            self.player2.direction.y = 1 if self.ball.position.y > self.player2.position.y else -1

        self.player2.direction = self.player2.direction if self.ai else Vector2(x_player2, y_player2)

        x_player1 = self.player1.axis_smoothing(self.player1.direction.x, self.player1.target_direction.x, deltaTime)
        y_player1 = self.player1.axis_smoothing(self.player1.direction.y, self.player1.target_direction.y, deltaTime) 
        self.player1.direction = Vector2(x_player1, y_player1)
        
async def main() -> None:
    deltaTime: float = 0.0
    clock = pygame.time.Clock()
    game = PyPong()
    while True:
        game.render()
        game.handle_input()
        game.update(deltaTime)

        deltaTime = clock.tick(120) / 1000
        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())