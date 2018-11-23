from time import time
from math import sqrt

from enemy import Enemy
from thrown import ThrownObject
from load_image import load_image
from random_between import random_between
from config import *


class Ranger(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hit_image = 'ranger_hit_particle.png'
        self.death_image = 'ranger_death_particle.png'
        self.last_shot = time()

    def update(self):
        super().update()
        self.maybe_shoot()

    def maybe_shoot(self):
        cur_time = time()
        if cur_time - self.last_shot < RANGER_COOLDOWN:
            return False
        self.last_shot = cur_time
        return self.shoot()

    def shoot(self):
        player = self.game.get_nearest_player(self.rect.center)
        vy = random_between(RANGER_SHOOT_MIN_YSPEED, RANGER_SHOOT_MAX_YSPEED)
        g = self.gravity
        xe, ye = self.rect.center
        xp, yp = player.rect.center
        
        vx = (xp - xe) * g / (2 * vy)
        thrown = ThrownObject(game=self.game, gravity=g, pos=self.rect.center, speed=[vx, -vy])
        self.game.add_sprite(thrown)

