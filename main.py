import sys
import pygame
from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import TileMap


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Paciak RPG")
        self.screen = pygame.display.set_mode((1024, 768))
        self.display = pygame.Surface((512, 384))

        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        self.assets = {
            "decor": load_images('tiles/decor'),
            "grass": load_images('tiles/grass'),
            "large_decor": load_images('tiles/large_decor'),
            "stone": load_images('tiles/stone'),
            "player": load_image('player/player.png')
        }

        self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))

        self.tilemap = TileMap(self, tile_size=16)

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.fill((255, 255, 255))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
