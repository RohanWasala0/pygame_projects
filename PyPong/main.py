import sys, platform
import asyncio
import pygame
import random
from math import hypot
from functools import wraps

from utils import *
from Script.ball import Ball
from Script.paddle import Paddle
from Script.settings import Settings
from text_canvas import text_canvas as tc
from input_manager import InputManager

if sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"

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
        self.display = pygame.display.set_mode(SCREEN_SIZE, pygame.SRCALPHA|pygame.SCALED)
        self.screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.screen_group = pygame.sprite.Group()
        self.screen_input_manager = InputManager()

        self.is_playing = True
        self.is_running = True
        self.player1_score = 0
        self.player2_score = 0
        self.time = 0

        self.hit = pygame.mixer.Sound(HIT)
        self.point = pygame.mixer.Sound(POINT)

        self._initialize_text_canvas()
        self._initialize_objects()
        [print(f"\n{x}") for x in self.screen_group.spritedict]

        self.screen_input_manager.input_chart = {
            'discrete': {
                pygame.QUIT: self.quit,
                pygame.KEYDOWN: {
                    pygame.K_r: self.reset_game,
                    pygame.K_SPACE: lambda: [x.kill() for x in (self.player1_control_text, self.player2_control_text, self.start_play_text)]
                }
            },
        }

    def _initialize_objects(self) -> None:
        self.ball = Ball(
            groups= self.screen_group,
            anchor= 'center',
            position= pygame.Vector2(WIDTH//2, HEIGHT//2),
            radius= 25,
            color= BALL_GREY,
        )

        self.player1 = Paddle(
            groups= self.screen_group,
            keys= (pygame.K_w, pygame.K_s),
            zone= (0.0, 0.5, 0.0, 1.0),
            anchor= 'center',
            position= pygame.Vector2(60, HEIGHT//2),
            dimensions= (40, 150),
            color= PADDLE_BROWN,
        )
        self.player2 = Paddle(
            groups= self.screen_group,
            keys= (pygame.K_UP, pygame.K_DOWN),
            zone= (0.5, 1.0, 0.0, 1.0),
            anchor= 'center',
            position= pygame.Vector2(WIDTH - 60, HEIGHT//2),
            dimensions= (40, 150),
            color= PADDLE_BROWN,
        )
        self.settings_menu = Settings(
            groups= self.screen_group,
            anchor= 'center',
            position= pygame.Vector2(WIDTH//2, HEIGHT//2),
            dimensions= (WIDTH-(40*4), HEIGHT-(40*2)),
            color= PADDLE_BROWN,
        )

    def _initialize_text_canvas(self) -> None:

        self.player1_control_text = tc(
            raw= f"[position: 20, (40*8)+20][size: 20][color: {PARTICLES_BEIGE.hex}][align: left][text: 'S','W'\nto move]",
            font_path= FONT_PATH,
            groups= self.screen_group,
        )
        self.player2_control_text = tc(
            f"[position: {WIDTH}-20, (40*8)+17][size: 20][color: white][align: right][text: 'UP','DOWN'\nto move]",
            font_path= FONT_PATH,
            groups= self.screen_group,
            anchor= 'topright'
        )
        self.score = tc(
            raw= f"[position: {WIDTH}//2, 60][size: 25][color: white][align: center][text: {self.player2_score}-{self.player1_score}]",
            font_path= FONT_PATH,
            groups= self.screen_group,
            anchor= 'center'
        )
        self.start_play_text = tc(
            raw= f"[position: {WIDTH}//2, {HEIGHT}-60][size: 16][align: center][text: Press 'SPACE' to start]",
            font_path= FONT_PATH,
            groups= self.screen_group,
            anchor= 'center'
        )
        self.reset_text = tc(
            raw= f"[position: 20, 20][size: 15][align: left][text: 'R'\nto Reset]",
            font_path= FONT_PATH,
            groups= self.screen_group,
        )

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
        # self.screen.blit(animated_texture, (0, 0))

        self.dotted_line(self.screen)

        self.ball.draw_trail(self.screen)
        self.screen_group.draw(self.screen)

        self.display.blit(self.screen)

    def handle_input(self) -> None:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        self.screen_input_manager.handle_input(events, keys)
        self.ball.input_manager.handle_input(events, keys)
        self.player1.input_manager.handle_input(events, keys)
        self.player2.input_manager.handle_input(events, keys)

    def update(self, deltaTime: float) -> None:

        self.time += 40 * deltaTime
        self.screen_group.update(deltaTime)
        self.paddle_collision()

        # self.player1_control_text.sinusoidal_motion( 9, 0.18, 25)
        # self.player2_control_text.sinusoidal_motion( 9, 0.18, 25)
        # self.start_play_text.sinusoidal_motion( -9, 0.18, 25)

        if not self.is_playing:
            self.ball.input_manager.input_chart['touch'] = {}
            
        self.is_playing = True if self.ball.velocity == pygame.Vector2() else False
        # self.hit.play() if self.ball.collision_walls( ) else None
        # self.point_scored()
        # self.text_canvas_group.update(deltaTime)

    def paddle_collision(self) -> None:

        def handle_collision(paddle, direction, angle_range):
            angles = [angle + random.randint(-10, 10) for angle in angle_range]

            self.ball.velocity = self.ball.change_angle(angles)

        if self.player1.rect.colliderect(self.ball.rect):
            handle_collision(self.player1, -1, [315, 405]) if self.ball.position.x > 63 else None
            self.hit.play()
        elif self.player2.rect.colliderect(self.ball.rect):
            handle_collision(self.player2, 1, [135, 225]) if self.ball.position.x < WIDTH-63 else None
            self.hit.play()
    
    def point_scored(self) -> None:
        if self.ball.position.x < self.ball.radius:
            self.player1_score += 1
            self.ball.reset()
            self.is_playing = not self.is_playing
            print(self.ball.position, self.ball.rect.center)
            self.text_canvas_group.add(self.start_play)
            self.point.play()
        elif self.ball.position.x > WIDTH - self.ball.radius:
            self.player2_score += 1
            self.ball.reset()
            self.is_playing = not self.is_playing
            print(self.ball.position, self.ball.rect.center)
            self.text_canvas_group.add(self.start_play)
            self.point.play()

    def reset_game(self):
        self.ball.reset()
        self.player1.reset()
        self.player2.reset()
        self.player1_score, self.player2_score = 0, 0
        self.screen_group.add(self.player1_control_text, self.player2_control_text, self.start_play_text)

    def dotted_line(self, surface:pygame.Surface):
        x1, y1 = pygame.Vector2(WIDTH//2, 0)
        x2, y2 = pygame.Vector2(WIDTH//2, HEIGHT)

        dist = hypot(x2-x1, y2-y1)
        dx, dy = (x2 - x1)/dist, (y2-y1)/dist
        for i in range(0, int(dist), 10):
            start_pos = x1 + dx*i, y1 + dy*i
            end_pos = x1 + dx*(i+5), y1 + dy*(i+5)
            pygame.draw.line(surface, pygame.Color('white'), start_pos, end_pos)

    def quit(self):
        print('Shutting Down')
        pygame.quit()
        sys.exit()

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