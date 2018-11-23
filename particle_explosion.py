from math import pi, sin, cos

from pygame.sprite import Sprite

from particle import Particle
from random_between import random_between


def particle_explosion(game, image, pos, min_speed, max_speed, min_lifespan, max_lifespan, count):
    for i in range(count * 15):
        angle = random_between(0.0, 2 * pi)
        speed = random_between(min_speed, max_speed) * 15
        vx = sin(angle) * speed
        vy = cos(angle) * speed
        particle = Particle(
            image=image,
            game=game,
            pos=pos,
            speed=[vx, vy],
            lifespan=random_between(min_lifespan, max_lifespan) * 3
        )
        game.add_sprite(particle)
