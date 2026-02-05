import sys
import pygame

from scripts.utilities import image, images

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.imgs = {
            "dirt": images("tiles/dirt"),
            "flowers": images("tiles/decor/flowers"),
            "large_decor": images("tiles/decor/large_decors"),
            "spikes": images("tiles/spikes"),
            "player": image("tiles/character_spawn/1.png")
        }

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)

Game().run()