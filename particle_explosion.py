from math import pi, sin, cos

from pygame.sprite import Sprite

from particle import Particle
from random_between import random_between
from config import *


def particle_explosion(game, image, pos, min_speed, max_speed, min_lifespan, max_lifespan, count):
    for i in range(round(count * PARTICLE_COUNT_SCALE)):
        angle = random_between(0.0, 2 * pi)
        speed = random_between(min_speed, max_speed) * PARTICLE_SPEED_SCALE
        vx = sin(angle) * speed
        vy = cos(angle) * speed
        particle = Particle(
            image=image,
            game=game,
            pos=pos,
            speed=[vx, vy],
            lifespan=random_between(min_lifespan, max_lifespan) * PARTICLE_LIFETIME_SCALE
        )
        game.add_sprite(particle)
