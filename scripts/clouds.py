import random


class Cloud:

    def __init__(self, position, img, speed, depth):
        self.position = list(position)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.position[0] += self.speed

    def render(self, surface, offset=(0, 0)):
        render_pos = (self.position[0] - offset[0] * self.depth, self.position[1] - offset[1] * self.depth)
        surface.blit(self.img, (render_pos[0] % (surface.get_width() + self.img.get_width()) - self.img.get_width(),
                                render_pos[1] % (surface.get_height() + self.img.get_height()) - self.img.get_height()))


class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds_list = []

        for _ in range(count):
            self.clouds_list.append(Cloud((random.random() * 99999, random.random() * 9999),
                                          random.choice(cloud_images), random.random() * 0.05 + 0.05,
                                          random.random() * 0.6 + 0.2))

        self.clouds_list.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds_list:
            cloud.update()

    def render(self, surface, offset=(0, 0)):
        for cloud in self.clouds_list:
            cloud.render(surface, offset=offset)
