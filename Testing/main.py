import pygame
import asyncio
import math
import sys

# Configuration and Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PARTICLE_RADIUS = 10
AMPLITUDE = 15  # Amplitude of the sinusoidal motion
FREQUENCY = 0.18  # Frequency of the sinusoidal motion
CENTER_Y = SCREEN_HEIGHT // 2
CENTER_X = SCREEN_WIDTH // 2
BACKGROUND_COLOR = (30, 30, 30)
PARTICLE_COLOR = (255, 100, 100)
TRAIL_COLOR = (100, 100, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Particle Simulation")
clock = pygame.time.Clock()


class Particle:
    def __init__(self, x, amplitude, frequency):
        self.x = x
        self.amplitude = amplitude
        self.frequency = frequency
        self.speed = 25
        self.time = 0
        print("hahahah")
        self.trail = []

    def update(self, dt):
        self.time += dt * self.speed
        self.y = CENTER_Y + self.amplitude * math.sin(self.frequency * self.time)
        self.trail.append((self.x + self.time, self.y))

    def draw(self, surface):
        for i in range(1, len(self.trail)):
            pygame.draw.line(surface, TRAIL_COLOR, self.trail[i - 1], self.trail[i], 2)
        pygame.draw.circle(surface, PARTICLE_COLOR, (int(self.x), int(self.y)), PARTICLE_RADIUS)


async def main():
    particle = Particle(CENTER_X, AMPLITUDE, FREQUENCY)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill(BACKGROUND_COLOR)

        # Update particle position
        dt = clock.get_time() / 1000  # Delta time in seconds
        particle.update(dt)

        # Draw particle
        particle.draw(screen)

        # Refresh display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)
        await asyncio.sleep(0)  # Yield to event loop

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())
