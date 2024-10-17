import sys
import pygame
import pygame.freetype as ft
import random
import math

from Script.Menu import Menu
from Script.Paddle import Paddle
from Script.ball import Ball
from Script.particles import Particles

FONT_PATH = 'SixtyfourConvergence-Regular-VariableFont_BLED,SCAN,XELA,YELA.ttf'
#Colors
BLACK = pygame.Color(0,0,0)
BACKGROUND_BLACK = pygame.Color('#181C14')
PADDLE_BROWN = pygame.Color('#3C3D37')
BALL_GREY = pygame.Color('#697565')
PARTICLES_BEIGE = pygame.Color('#ECDFCC')

WIDTH, HEIGHT = 640, 480

class Pong:

    def __init__(self, Screen_DIMENSIONS: list) -> None:
        pygame.init()
        pygame.display.set_caption("Game")

        self.font20 = pygame.font.Font(FONT_PATH, 20)
        self.ftFont = ft.Font(FONT_PATH, 20)
        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.clock = pygame.time.Clock()      
        self.tempVar = pygame.math.Vector2()
        self.particleGroup = pygame.sprite.Group()
        self.menuBool = False
        self.timerBool = False
        self.aiBool = True

        #region Player
        self.paddleGroup = pygame.sprite.Group()
        self.player1 = Paddle(groups=self.paddleGroup, tag='player', position=pygame.math.Vector2(40, HEIGHT/2), entitySize=(40, 150), color=PADDLE_BROWN, input_keys=[pygame.K_w, pygame.K_s])
        self.player1_score = 0
        self.player2 = Paddle(groups=self.paddleGroup, tag='player', position=pygame.math.Vector2(WIDTH - 40, HEIGHT/2), entitySize=(40, 150), color=PADDLE_BROWN, input_keys=[pygame.K_UP, pygame.K_DOWN])
        self.player2_score = 0
        #endregion
        #region Ball
        self.ballGroup = pygame.sprite.Group()
        self.ball = Ball(groups=self.ballGroup, tag='ball', position=pygame.math.Vector2(WIDTH/2, HEIGHT/2), entitySize=25, color=BALL_GREY)
        #endregion
        #region Menu 
        self.menuGroup = pygame.sprite.Group()
        PARTICLES_BEIGE.a = 128
        self.menu = Menu(game=self, groups=self.menuGroup, tag='menu', position=pygame.math.Vector2(WIDTH/2, HEIGHT/2), entitySize=(WIDTH - 100, HEIGHT - 100), color=PARTICLES_BEIGE)
        #endregion
        
    #Render function to draw surfaces onto display
    def render(self):
        self.screen.fill(BACKGROUND_BLACK)
        pygame.draw.line(self.screen, BLACK, (WIDTH/2, 0), (WIDTH/2, HEIGHT))
        pygame.draw.line(self.screen, BLACK, (0, HEIGHT/2), (WIDTH, HEIGHT/2))
        
        self.paddleGroup.draw(self.screen)
        self.ballGroup.draw(self.screen)
        self.particleGroup.draw(self.screen)
        
        # self.textComp(self.screen, self.font20, f'{self.player1_score} - {self.player2_score}', BLACK, 20, [320, 120])
        self.ftFont.render_to(self.screen, self.screen.get_rect(), f'{self.player1_score} - {self.player2_score}')
        
        if self.menuBool:
            self.menuGroup.draw(self.screen)
            self.menu.UImanager.draw_ui(self.screen)
    
    #
    def eventHandling(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.timerBool = True
                self.toggleMenu()
            if event.key == pygame.K_p:
                for x in range(200): self.spawnParticle()
            
        self.ball.handleInput(event)
        
        
        self.player1.handleInput(event)
        self.player2.handleInput(event)
        self.menu.handleInput(event)
        
        self.menu.UImanager.process_events(event)
     
    #   
    def update(self):
        time_delta = self.clock.tick() / 1000.0
        
        self.ballGroup.update() if not self.menuBool else None
        self.player1.update()  
        self.paddleCollision()
        self.Score()
        self.player2.computerPaddle(self.ball.position) if self.aiBool else self.player2.update()
        self.particleGroup.update()
        self.menu.UImanager.update(time_delta)

#Spawn particles
    def spawnParticle(self, pos: pygame.math.Vector2, clampAngles: list[int, int]):
        angle = random.uniform(math.radians(clampAngles[0]), math.radians(clampAngles[1]))
        direction = pygame.math.Vector2(math.cos(angle), math.sin(angle)).normalize()
        PARTICLES_BEIGE.a = 255
        Particles(groups=self.particleGroup, tag='particle', position=pos, direction=direction, entitySize=4, color=PARTICLES_BEIGE) 
        
#bounce in random direction after hitting a paddle     
    def paddleCollision(self):
        if (
            (self.ball.position.x + self.ball.radius) >= self.player1.position.x  or 
            (self.ball.position.x + self.ball.radius) <= self.player2.position.x
        ):
            if self.player1.rect.colliderect(self.ball.rect):
                self.ball.change_angle([315, 405])
                for x in range(20): self.spawnParticle(pygame.math.Vector2(self.ball.position.x - self.ball.radius, self.ball.position.y), [315, 405])
                
            elif self.player2.rect.colliderect(self.ball.rect):
                self.ball.change_angle([135, 225])
                for x in range(20): self.spawnParticle(pygame.math.Vector2(self.ball.position.x + self.ball.radius, self.ball.position.y), [135, 225])

#Count score
    def Score(self):
        if (self.ball.position.x - self.ball.radius -2) <= 0:
            self.player2_score += 1
            self.ball.reset()
        
        elif (self.ball.position.x - self.ball.radius -2) >= WIDTH:
            self.player1_score += 1
            self.ball.reset()
        
    def run(self, GAME_FPS: int):
        while True:
            
            self.render()
        
            for event in pygame.event.get():
                self.eventHandling(event) 
            
            self.update()
            
            pygame.display.update()  
            self.clock.tick(GAME_FPS)     
       
    def toggleMenu(self):   
        if self.menuBool:
            self.lastTime = pygame.time.get_ticks()
            self.ball.direction = self.tempVar
            self.menuBool = False
        else:
            self.tempVar = self.ball.direction
            self.ball.direction = pygame.math.Vector2()
            self.menuBool = True
            
    def timer(self, TTime):
        curretTime = pygame.time.get_ticks()
        if curretTime - self.lastTime > TTime * 1000:
            self.lastTime = curretTime
            return True
        else:
            return False
    
def print_attributes(obj):
    for attribute, value in obj.__dict__.items():
        print(f"{attribute}: {value}")


            
if __name__ == "__main__":
    Pong(Screen_DIMENSIONS=(640, 480)).run(GAME_FPS=60)