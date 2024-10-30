import sys
import pygame
from random import choice

from entity import Entity

WIDTH = 699
HEIGHT = 699

#Colors
BACKGROUND_BLACK = pygame.Color('#181C14')
BIT_BLUE_DARK = pygame.Color('#0d132a')
BIT_BLUE_LIGHT = pygame.Color('#adc3e8')

class Template:

    def __init__(self, Screen_DIMENSIONS: list) -> None:
        pygame.init()
        pygame.display.set_caption("WFC")

        #system variables 
        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.clock = pygame.time.Clock()
        self.deltaTime = 0
        
        #game variables
        self.activate = False
        self.DIM = 36
        
        #Sprite group
        self.tilesGroup = pygame.sprite.Group()

        #game objects
        
        #region Enitities
        self.blank = Entity(
            tag='blank',
            entitySize=36,
            color=[BIT_BLUE_DARK, BIT_BLUE_LIGHT],
            pattern=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        )
        self.up = Entity(
            tag='up',
            entitySize=36,
            color=[BIT_BLUE_DARK, BIT_BLUE_LIGHT],
            pattern=[[0, 1, 0], [1, 1, 1], [0, 0, 0]]
        )
        self.down = Entity(
            tag='down',
            entitySize=36,
            color=[BIT_BLUE_DARK, BIT_BLUE_LIGHT],
            pattern=[[0, 0, 0], [1, 1, 1], [0, 1, 0]]
        )
        self.right = Entity(
            tag='right',
            entitySize=36,
            color=[BIT_BLUE_DARK, BIT_BLUE_LIGHT],
            pattern=[[0, 1, 0], [0, 1, 1], [0, 1, 0]]
        )
        self.left = Entity(
            tag='left',
            entitySize=36,
            color=[BIT_BLUE_DARK, BIT_BLUE_LIGHT],
            pattern=[[0, 1, 0], [1, 1, 0], [0, 1, 0]]
        )
        #endregion
        self.tileSet = [self.blank, self.up, self.down, self.right, self.left]
        self.grid = self.make_grid(self.DIM)
                
    def render(self):
        self.screen.fill(BACKGROUND_BLACK)
        
        self.tilesGroup.draw(self.screen)
        pass
    
    def eventHandling(self, event: pygame.event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.activate = True
        pass
    
    def update(self):
        self.tilesGroup.update()
        pass
        
    def run(self, GAME_FPS: int):
        last_time = pygame.time.get_ticks()
        while True:
            self.deltaTime = self.clock.tick(GAME_FPS)/ 1000
            #Render
            self.render()
            
            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.eventHandling(event)

            current_time = pygame.time.get_ticks()
            if current_time - last_time > 50 and self.activate:

                self.evaluate_entropy()
                self.drawPattern(self.DIM)
                if len(self.tilesGroup.sprites()) == (self.DIM*self.DIM)-1:
                    self.activate = False
            #print([(x['collapsed'], [y.tag for y in x['options']]) for x in self.grid])
                self.update_options(self.DIM)
            #print([(x['collapsed'], [y.tag for y in x['options']]) for x in self.grid])
                last_time = current_time
                
                
            self.update()
                
            pygame.display.update()
    
    def make_grid(self, dimension: int) -> list[dict]:
        return [
            {
                'collapsed': False,
                'options': self.tileSet,
            } for i in range(dimension*dimension)
        ]
      
    def drawPattern(self, dimension: int) -> None:
        w = WIDTH//dimension
        h = HEIGHT//dimension      
          
        for y in range(dimension):
            for x in range(dimension):
                cell = self.grid[x+y * dimension]
                if cell['collapsed']:
                    tile = cell['options'][0].copy(pygame.Vector2(x* w, y* h))
                    tile.image = pygame.transform.scale(tile.image, (w, h))
                    self.tilesGroup.add(tile)

    def evaluate_entropy(self) -> None:
        min_len = min(len(x['options']) for x in self.grid if not x['collapsed'])
        gridCopy = [x for x in self.grid if len(x['options']) == min_len and not x['collapsed']]
        cell = choice(gridCopy)
        cell['collapsed'] = True
        cell['options'] = [choice(cell['options'])]
        pass
            
    def update_options(self, dimension: int):
        for index, tile in enumerate(self.grid):
            if not tile['collapsed']:
                continue
            up = self.grid[index-dimension] if 0 < index-dimension < dimension*dimension else None
            down = self.grid[index+dimension] if 0 < index+dimension < dimension*dimension else None
            right = self.grid[index+1] if 0 < index+1 < dimension*dimension else None
            left = self.grid[index-1] if 0 < index-1 < dimension*dimension else None
            #up condition
            if up and not up['collapsed']:
                up['options'] = [a for a in up['options'] if a.pattern[2][1] == tile['options'][0].pattern[0][1]]
            # #down condition
            if down and not down['collapsed']:
                down['options'] = [a for a in down['options'] if a.pattern[0][1] == tile['options'][0].pattern[2][1]]
            # #right condition
            if right and not right['collapsed']:
                right['options'] = [a for a in right['options'] if a.pattern[1][0] == tile['options'][0].pattern[1][2]]
            # #left condition
            if left and not left['collapsed']:
                left['options'] = [a for a in left['options'] if a.pattern[1][2] == tile['options'][0].pattern[1][0]]

Template(Screen_DIMENSIONS=(WIDTH, HEIGHT)).run(GAME_FPS=60)