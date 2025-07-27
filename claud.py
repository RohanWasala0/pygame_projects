import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GRAY = (128, 128, 128)

# Using pygame's built-in Vector2 class

class Ball:
    def __init__(self, x, y, radius=15):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(random.uniform(-8, 8), random.uniform(-8, 8))
        self.radius = radius
        self.color = RED
        self.trail = []
        self.max_trail_length = 20
    
    def update(self):
        # Update position (no gravity or friction)
        self.pos += self.vel
        
        # Add to trail
        self.trail.append((int(self.pos.x), int(self.pos.y)))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

    def check_wall_collision(self):
        # Left wall
        if self.pos.x - self.radius <= 0:
            self.pos.x = self.radius
            self.vel.x = -self.vel.x 

        # Right wall
        if self.pos.x + self.radius >= WIDTH:
            self.pos.x = WIDTH - self.radius
            self.vel.x = -self.vel.x 

        # Top wall
        if self.pos.y - self.radius <= 0:
            self.pos.y = self.radius
            self.vel.y = -self.vel.y 

        # Bottom wall
        if self.pos.y + self.radius >= HEIGHT:
            self.pos.y = HEIGHT - self.radius
            self.vel.y = -self.vel.y
    
    def check_square_collision(self, square, screen):
        # Predictive collision for dynamic square
        future_pos = self.pos + self.vel
    
        rect = square.get_rect()

        closest_x = max(rect.left, min(future_pos.x, rect.right))
        closest_y = max(rect.top, min(future_pos.y, rect.bottom))
        print(closest_x, closest_y)
        pygame.draw.circle(screen, pygame.Color('red'), (int(closest_x), int(closest_y)), 5, 5)

        distance_vec = future_pos - pygame.math.Vector2(closest_x, closest_y)
        distance = distance_vec.length()

        if distance < self.radius:
            normal = distance_vec.normalize() if distance != 0 else pygame.math.Vector2(1, 0)
            overlap = self.radius - distance
            self.pos += normal * overlap
            self.vel = self.vel.reflect(normal)

    
    def draw(self, screen):
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = i / len(self.trail)
            trail_color = (int(self.color[0] * alpha), 
                          int(self.color[1] * alpha), 
                          int(self.color[2] * alpha))
            pygame.draw.circle(screen, trail_color, pos, max(1, int(self.radius * alpha * 0.5)))
        
        # Draw ball
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius, 2)
        
        # Draw velocity vector (for visualization)
        end_x = int(self.pos.x + self.vel.x * 3)
        end_y = int(self.pos.y + self.vel.y * 3)
        pygame.draw.line(screen, WHITE, (int(self.pos.x), int(self.pos.y)), (end_x, end_y), 2)

class Square:
    def __init__(self, x, y, width, height):
        self.pos = pygame.math.Vector2(x, y)
        self.width = width
        self.height = height
        self.color = BLUE
        self.speed = 5
        self.vel = pygame.math.Vector2(0, 0)
    
    def update(self, keys):
        self.vel = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]:
            self.vel.y = -self.speed
        if keys[pygame.K_s]:
            self.vel.y = self.speed
        if keys[pygame.K_a]:
            self.vel.x = -self.speed
        if keys[pygame.K_d]:
            self.vel.x = self.speed
        self.pos += self.vel

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.pos, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (*self.pos, self.width, self.height), 3)

    def get_rect(self):
        return pygame.Rect(*self.pos, self.width, self.height)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Physics Ball Bounce Simulation")
    clock = pygame.time.Clock()
    
    # Create objects
    ball = Ball(100, 100)
    square = Square(WIDTH//2 - 50, HEIGHT//2 - 50, 100, 100)
    
    # Font for displaying info
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset ball with random position and velocity
                    ball = Ball(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50))
                elif event.key == pygame.K_r:
                    # Reset to original position
                    ball = Ball(100, 100)
        
        keys = pygame.key.get_pressed()
        square.update(keys)
        
        # Update physics
        ball.update()
        ball.check_wall_collision()
        
        # Draw everything
        screen.fill(BLACK)
        ball.check_square_collision(square, screen)
        
        # Draw grid for reference
        for i in range(0, WIDTH, 50):
            pygame.draw.line(screen, (30, 30, 30), (i, 0), (i, HEIGHT))
        for i in range(0, HEIGHT, 50):
            pygame.draw.line(screen, (30, 30, 30), (0, i), (WIDTH, i))
        
        square.draw(screen)
        ball.draw(screen)
        
        # Display info
        speed = ball.vel.length()
        speed_text = font.render(f"Speed: {speed:.1f}", True, WHITE)
        pos_text = font.render(f"Pos: ({ball.pos.x:.0f}, {ball.pos.y:.0f})", True, WHITE)
        vel_text = font.render(f"Vel: ({ball.vel.x:.1f}, {ball.vel.y:.1f})", True, WHITE)
        
        screen.blit(speed_text, (10, 10))
        screen.blit(pos_text, (10, 50))
        screen.blit(vel_text, (10, 90))
        
        # Instructions
        inst_text = font.render("SPACE: New Ball | R: Reset", True, GRAY)
        screen.blit(inst_text, (10, HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()