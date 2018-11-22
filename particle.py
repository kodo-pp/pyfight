from time import time

from pygame.sprite import Sprite

from load_image import load_image


class Particle(Sprite):
    def __init__(self, image, game, speed, pos, lifespan):
        super().__init__()
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = speed
        self.last_time = time()
        self.dead = False
        self.game = game
        self.end_life = time() + lifespan
        self.pos = list(pos)

    def update(self):
        cur_time = time()
        if cur_time >= self.end_life:
            self.die()
            return
        delta_time = cur_time - self.last_time
        self.last_time = cur_time

        self.pos[0] += delta_time * self.speed[0]
        self.pos[1] += delta_time * self.speed[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def die(self):
        self.dead = True

