from time import time

from pygame.sprite import Sprite

from load_image import load_image
from enemy import Enemy


class Laser(Sprite):
    def __init__(self, game, speed, pos):
        super().__init__()
        self.image = load_image('laser.png')
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = speed
        self.last_time = time()
        self.dead = False
        self.game = game

    def update(self):
        cur_time = time()
        delta_time = cur_time - self.last_time
        self.last_time = cur_time
        self.rect.x += delta_time * self.speed[0]
        self.rect.y += delta_time * self.speed[1]
        self.maybe_hit_enemy()
        self.maybe_leave_screen()

    def maybe_hit_enemy(self):
        for sprite in self.game.sprites:
            if self.rect.colliderect(sprite.rect) and isinstance(sprite, Enemy):
                sprite.hit_by(self)
                self.die()
                return True
        return False

    def maybe_leave_screen(self):
        if self.rect.right < 0 or self.rect.left > self.game.width:
            self.die()
            return True
        return False

    def die(self):
        self.dead = True

