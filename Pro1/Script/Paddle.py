import pygame
from pygame.sprite import Group
from random import uniform, random, randint

from .entities import Entity

class Paddle(Entity, pygame.sprite.Sprite):
    def __init__(self,
            groups: Group, 
            tag: str, 
            input_keys: list,
            position: pygame.Vector2 = pygame.math.Vector2(), 
            direction: pygame.Vector2 = pygame.math.Vector2(), 
            entitySize: tuple = (0, 0), 
            color: pygame.Color = pygame.Color('black')) -> None:
        super().__init__(groups, tag, position, direction, entitySize, color)

        self.speed = 5
        self.reaction_delay = 4
        self.reaction_counter = 0
        
        self.inputChart = {
            pygame.KEYDOWN: {
                input_keys[0] : lambda: setattr(self, "direction", pygame.Vector2(0, -1)),
                input_keys[1] : lambda: setattr(self, "direction", pygame.Vector2(0, 1)),
                },
            pygame.KEYUP: {
                input_keys[0] : lambda: setattr(self, "direction", pygame.Vector2(0, 0)),
                input_keys[1] : lambda: setattr(self, "direction", pygame.Vector2(0, 0)),
                },
        }
        
        self.image = pygame.Surface(size=self.entitySize).convert_alpha()
        self.image.set_colorkey('black')
        self.render()
        
    def update(self):
        self.position += self.direction * self.speed
        
        self.rect.center = self.position
        return super().update()
    
    def render(self):
        
        self.rect = pygame.Rect((0,0), self.entitySize)
        
        pygame.draw.rect(surface=self.image, color=self.color, rect=self.rect)
        self.rect = self.image.get_rect(center=self.position)
        
        return super().render()

    def computerPaddle(self, ballPosition, difficulty = 0):
        # if self.reaction_counter < self.reaction_delay:
        #     self.reaction_counter += 1
        # else:
        #     self.reaction_counter = 0
            
        #     if self.position.y < ballPosition.y:
        #         self.position.y = min(self.speed, abs(self.position.y- ballPosition.y))
        #     elif self.position.y > ballPosition.y:
        #         self.position.y = min(self.speed, abs(self.position.y- ballPosition.y))
                
        
        #print(pygame.math.lerp(self.position.y, ballPosition.y, 0.6))
        self.position.y = pygame.math.lerp(self.position.y , ballPosition.y, 0.2)
        # #self.position.y = ballPosition.y
        self.rect.center = self.position
    
    # def computerPaddle(self, ball, difficulty=0.1):
    #     ball_y = ball.position.y
    #     paddle_y = self.position.y
    #     error_margin = randint(-20, 20)
        
    #     if paddle_y < ball_y + error_margin:
    #         self.direction = pygame.Vector2(0, 1)
    #     elif paddle_y > ball_y + error_margin:
    #         self.direction = pygame.Vector2(0, -1)
    #     else:
    #         self.direction = pygame.Vector2(0, 0)
        
    #     # Introduce difficulty: only update direction sometimes
    #     if uniform(0, 1) > difficulty:
    #         self.direction = pygame.Vector2(0, 0)

    #     self.position += self.direction * self.speed
    #     self.rect.center = self.position
    #     return super().update()
    
    def computerPaddle(self, ballPosition, difficulty = 1):
        """ Makes the paddle follow the ball with some imperfections. """
        # Get the y position of the ball
        ball_y = ballPosition.y
        error_margin = randint(-20, 20)
        # Introduce some randomness/inaccuracy based on difficulty
        max_speed = self.speed * (difficulty + uniform(-0.2, 0.2))
        
        # Make the paddle "lazy" by only moving if the ball is a certain distance away
        if abs(self.position.y - ball_y) > 10:
            if self.position.y < ball_y + error_margin:
                self.position += min(max_speed, ball_y - self.position.y) * pygame.Vector2(0, 1) # Move paddle down
            elif self.position.y > ball_y + error_margin:
                self.position += min(max_speed, self.position.y - ball_y) * pygame.Vector2(0, -1)# Move paddle up
            else:
                self.position += min(max_speed, self.position.y - ball_y) * pygame.Vector2()

        # # Add additional randomness to simulate mistakes (lower difficulty makes bigger mistakes)
        # if random.random() > self.difficulty:
        #     self.position.y += random.uniform(-10, 10)  # Random nudge
        self.rect.center = self.position
        
        #     predicted_ball_center_y = ball.position.y + ball.direction[1] * self.speed

        # # Introduce random offset and reaction delay based on difficulty
        # offset = random.uniform(-self.difficulty, self.difficulty)
        # reaction_delay = random.uniform(0, self.difficulty / 10)

        # # Target position for the paddle center with offset
        # target_center_y = predicted_ball_center_y + offset

        # # Move towards target position with speed and reaction delay
        # if target_center_y > self.position.y + reaction_delay:
        #     self.direction.y = 1
        # elif target_center_y < self.position.y - reaction_delay:
        #     self.direction.y = -1
        # else:
        #     self.direction.y = 0