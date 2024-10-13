import sys
import pygame

from Script.Menu import Menu
from Script.Paddle import Paddle
from Script.ball import Ball

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
        self.font20 = pygame.font.Font('SixtyfourConvergence-Regular-VariableFont_BLED,SCAN,XELA,YELA.ttf', 20)

        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.fps = pygame.time.Clock()

        self.paddleGroup = pygame.sprite.Group()
        self.player1 = Paddle(groups=self.paddleGroup, tag='player', position=pygame.math.Vector2(40, HEIGHT/2), entitySize=(40, 150), color=PADDLE_BROWN, input_keys=[pygame.K_w, pygame.K_s])
        self.player1_score = 0
        self.player2 = Paddle(groups=self.paddleGroup, tag='player', position=pygame.math.Vector2(WIDTH - 40, HEIGHT/2), entitySize=(40, 150), color=PADDLE_BROWN, input_keys=[pygame.K_UP, pygame.K_DOWN])
        self.player2_score = 0
        
        self.ballGroup = pygame.sprite.Group()
        self.ball = Ball(groups=self.ballGroup, tag='ball', position=pygame.math.Vector2(WIDTH/2, HEIGHT/2), color=BALL_GREY)
        
        self.menuGroup = pygame.sprite.Group()
        PARTICLES_BEIGE.a = 128
        self.menu = Menu(groups=self.menuGroup, tag='menu', position=pygame.math.Vector2(WIDTH/2, HEIGHT/2), entitySize=(WIDTH - 100, HEIGHT - 100), color=PARTICLES_BEIGE)
    
    def textComp(self, displayText: str, textColor: tuple, textPosition: list = [0,0]):
        text = self.font20.render(displayText, True, textColor)
        textrect = text.get_rect()
        textrect.center = textPosition
        self.screen.blit(text, textrect)
        
    def run(self, GAME_FPS: int):
        menuBool = False
        while True:
            #Render
            self.screen.fill(BACKGROUND_BLACK)
            pygame.draw.line(self.screen, BLACK, (WIDTH/2, 0), (WIDTH/2, HEIGHT))
            pygame.draw.line(self.screen, BLACK, (0, HEIGHT/2), (WIDTH, HEIGHT/2))

            self.paddleGroup.draw(self.screen)
            self.ballGroup.draw(self.screen)
            
            self.textComp(f'{self.player1_score} - {self.player2_score}', BLACK, [320, 120])
            
            if menuBool:
                self.menuGroup.draw(self.screen)
                                    
            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menuBool = not menuBool
                    
                self.ball.handleInput(event)
                self.player1.handleInput(event)
                self.player2.handleInput(event)
                
                
            
            #game conditions
            #bounce in random direction after hitting a paddle
            if self.ball.position.x >= self.player1.position.x :
                if self.player1.rect.colliderect(self.ball.rect):
                    self.ball.direction.reflect_ip(self.ball.direction)
                    self.ball.change_angle([270, 450])
                    
                elif self.player2.rect.colliderect(self.ball.rect):
                    self.ball.direction.reflect_ip(self.ball.direction)
                    self.ball.change_angle([90, 270])
            
            # score counting logic
            if self.ball.position.x <= 0:
                self.ball.direction = pygame.math.Vector2()
                self.ball.position = pygame.math.Vector2(WIDTH/2, HEIGHT/2)
                self.player2_score += 1
            
            elif self.ball.position.x >= WIDTH:
                self.ball.direction = pygame.math.Vector2()
                self.ball.position = pygame.math.Vector2(WIDTH/2, HEIGHT/2)
                self.player1_score += 1
                
            #Update 
            self.ball.update()
            self.player1.update()            
            pygame.display.update()
            self.fps.tick(GAME_FPS)
            
            
            
Pong(Screen_DIMENSIONS=(640, 480)).run(GAME_FPS=60)