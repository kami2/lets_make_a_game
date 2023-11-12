import random
import math
import sys
import pygame
from scripts.entities import Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import TileMap
from scripts.clouds import Clouds
from scripts.particle import Particle


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Paciak RPG")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.display = pygame.Surface((960, 540))

        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        self.assets = {
            "clouds": load_images('clouds'),
            "decor": load_images('tiles/decor'),
            "grass": load_images('tiles/grass'),
            "large_decor": load_images('tiles/large_decor'),
            "stone": load_images('tiles/stone'),
            "player": load_image('player/player.png'),
            "background": load_image('other/background.png'),
            "player/idle": Animation(load_images('player/idle'), img_duration=6),
            "player/run": Animation(load_images('player/run'), img_duration=4),
            "player/jump": Animation(load_images('player/jump')),
            "player/slide": Animation(load_images('player/slide')),
            "particles/leaf": Animation(load_images('particles/leaf'), img_duration=20, loop=False)
        }

        self.clouds = Clouds(self.assets["clouds"], count=16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = TileMap(self, tile_size=16)
        self.tilemap.load('data/maps/map.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['position'][0], 4 + tree['position'][1], 23, 13))

        self.particles = []

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    position = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, particle_type="leaf",
                                                   position=position,
                                                   velocity=[-0.1, 0.3],
                                                   frame=random.randint(0, 20)))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == "leaf":
                    particle.position[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

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
