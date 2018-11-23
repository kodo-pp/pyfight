from time import time

from pygame.sprite import Sprite

from load_image import load_image
from enemy import Enemy
from particle_explosion import particle_explosion
from config import *


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
        particle_explosion(
            game=self.game,
            image='laser_particle.png',
            pos=self.rect.center,
            min_speed=LASER_PARTICLE_MIN_SPEED,
            max_speed=LASER_PARTICLE_MAX_SPEED,
            min_lifespan=LASER_PARTICLE_MIN_LIFETIME,
            max_lifespan=LASER_PARTICLE_MAX_LIFETIME,
            count=LASER_PARTICLE_COUNT
        )

