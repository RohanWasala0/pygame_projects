import sys, platform
import asyncio
import pygame
import random
from math import hypot

from utils import *
from Script.ball import Ball
from Script.paddle import Paddle
from Script.text_canvas import text_canvas

if sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"

class PyPong():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("PyPong")

        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SRCALPHA)
        self.clock = pygame.time.Clock()

        print("started")

        self._initialize_ball()
        self._initialize_paddles()
        self._initialize_text_canvas()
        self._grid_background()
        self.is_playing = True
        self.is_running = True

        self.hit = pygame.mixer.Sound(HIT)
        self.point = pygame.mixer.Sound(POINT)

    def _initialize_ball(self) -> None:
        self.ball_group = pygame.sprite.Group()
        self.ball = Ball(
            groups= self.ball_group,
            position= pygame.Vector2(WIDTH//2, HEIGHT//2),
            entity_size= (50, 50),
            color= BALL_GREY,
        )
        self.ball.input_chart.update({
            pygame.KEYDOWN: {
                pygame.K_SPACE: lambda: setattr(self.ball, 'velocity', self.ball.rand_velocity()),
            }
        })

    def _initialize_paddles(self) -> None:

        self.paddle_group = pygame.sprite.Group()
        self.player1 = Paddle(
            groups= self.paddle_group,
            position= pygame.Vector2(60, HEIGHT//2),
            entity_size= (40, 150),
            color= PADDLE_BROWN,
            input_keys= (pygame.K_w, pygame.K_s),
        )
        self.player1_score = 0
        self.player2= Paddle(
            groups= self.paddle_group,
            position= pygame.Vector2(WIDTH-60, HEIGHT//2),
            entity_size= (40, 150),
            color= PADDLE_BROWN,
            input_keys= (pygame.K_UP, pygame.K_DOWN),
        )
        self.player2_score = 0

    def _initialize_text_canvas(self) -> None:

        self.text_canvas_group = pygame.sprite.Group()
        self.player1_control_text = text_canvas(
            groups= self.text_canvas_group,
            position= pygame.Vector2(20, (40*8)+20),
            anchor= 'topleft',
            font_path= FONT_PATH,
            font_size= 20,
            color= pygame.Color('white'),
            text= f"'S', 'W'\nto move"
        )
        self.player1_control_text.input_chart.update({
            pygame.KEYDOWN:{
                pygame.K_SPACE: self.player1_control_text.kill
            }
        })
        self.player2_control_text = text_canvas(
            groups= self.text_canvas_group,
            position= pygame.Vector2((11* 40 ) + 20, (40*8)+20),
            anchor= 'topleft',
            font_path= FONT_PATH,
            font_size= 20,
            color= pygame.Color('white'),
            text= f"UP, DOWN\nto move"
        )
        self.player2_control_text.input_chart.update({
            pygame.KEYDOWN:{
                pygame.K_SPACE: self.player2_control_text.kill
            }
        })
        self.score_canvas = text_canvas(
            groups= self.text_canvas_group,
            position= pygame.Vector2((WIDTH//2), 60),
            anchor= 'center',
            font_path= FONT_PATH,
            font_size= 25,
            color= pygame.Color('white'),
        )  
        self.start_play= text_canvas(
            groups= self.text_canvas_group,
            position= pygame.Vector2(WIDTH//2, HEIGHT-60),
            anchor= 'center',
            font_path= FONT_PATH,
            font_size= 16,
            color= pygame.Color('white'),
            text= f"Press 'SPACE' to start"
        )
        self.start_play.input_chart.update({
            pygame.KEYDOWN:{
                pygame.K_SPACE: self.start_play.kill
            }
        })
        self.reset_text = text_canvas(
            groups= self.text_canvas_group,
            position= pygame.Vector2(20 ,20),
            anchor= 'topleft',
            font_path= FONT_PATH,
            font_size= 15,
            color= pygame.Color('white'),
            text= f"'R'\nto Reset"
        )
        self.reset_text.input_chart.update(
            {
                pygame.KEYDOWN: {
                    pygame.K_r : self.reset_game,
                }
            }
        )

    def _grid_background(self) -> None:
        self.background = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

        for x in range(0, WIDTH, 40):
            pygame.draw.line(self.background, pygame.Color(173, 170, 170, 75), (x, 0), (x, HEIGHT)) 
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(self.background, pygame.Color(173, 170, 170, 75), (0, y), (WIDTH, y)) 

    def render(self) -> None:
        self.screen.fill(BACKGROUND_BLACK)
        self.screen.blit(self.background, (0, 0))

        self.dotted_line(self.screen)

        self.ball_group.draw(self.screen)
        self.paddle_group.draw(self.screen)
        self.text_canvas_group.draw(self.screen)
        self.score_canvas.render()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.ball.handling_input(event) if self.is_playing else None
            self.player1.handling_input(event)
            self.player2.handling_input(event)
            self.player1_control_text.handling_input(event)
            self.player2_control_text.handling_input(event)
            self.start_play.handling_input(event)
            self.reset_text.handling_input(event)

    def update(self) -> None:
        deltaTime = self.clock.tick() / 1000.0

        self.paddle_collision()

        self.player1_control_text.sinusoidal_motion(deltaTime, 9, 0.18, 25)
        self.player2_control_text.sinusoidal_motion(deltaTime, 9, 0.18, 25)
        self.start_play.sinusoidal_motion(deltaTime, -9, 0.18, 25)

        self.ball_group.update(deltaTime)
        self.is_playing = True if self.ball.velocity == pygame.Vector2() else False
        self.paddle_group.update(deltaTime)
        self.hit.play() if self.ball.conditions() else None
        self.point_scored()
        self.text_canvas_group.update(deltaTime)

    def paddle_collision(self) -> None:

        def handle_collision(paddle, direction, angle_range):
            angles = [angle + random.randint(-10, 10) for angle in angle_range]
            randius_offset = direction * self.ball.radius

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
            self.ball.reset_position()
            self.is_playing = not self.is_playing
            print(self.ball.position, self.ball.rect.center)
            self.text_canvas_group.add(self.start_play)
            self.point.play()
        elif self.ball.position.x > WIDTH - self.ball.radius:
            self.player2_score += 1
            self.ball.reset_position()
            self.is_playing = not self.is_playing
            print(self.ball.position, self.ball.rect.center)
            self.text_canvas_group.add(self.start_play)
            self.point.play()
        self.score_canvas.text =  f"{self.player1_score}-{self.player2_score}"       

    def reset_game(self):
        self.ball.reset_position()
        self.player1.reset_position()
        self.player2.reset_position()
        self.player1_score, self.player2_score = 0, 0
        self.text_canvas_group.add(self.player1_control_text, self.player2_control_text)
    
    def dotted_line(self, surface:pygame.Surface):
        x1, y1 = pygame.Vector2(WIDTH//2, 0)
        x2, y2 = pygame.Vector2(WIDTH//2, HEIGHT)

        dist = hypot(x2-x1, y2-y1)
        dx, dy = (x2 - x1)/dist, (y2-y1)/dist
        for i in range(0, int(dist), 10):
            start_pos = x1 + dx*i, y1 + dy*i
            end_pos = x1 + dx*(i+5), y1 + dy*(i+5)
            pygame.draw.line(surface, pygame.Color('white'), start_pos, end_pos)


async def main() -> None:
    game = PyPong()
    while True:
        game.render()
        game.handle_input()
        game.update()

        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())