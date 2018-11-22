import random as rd
from time import time

from falling_sprite import FallingSprite
from load_image import load_image
from clamp import clamp
from sign_choose import sign_choose
from particle_explosion import particle_explosion

GRACE_PERIOD = 0.2

class Enemy(FallingSprite):
    def __init__(self, image, health, **kwargs):
        super().__init__(**kwargs)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.speed = [0, 0]
        self.hit_at = None
        self.health = health

    def maybe_hit_player(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.player.hit_by(self)
            return True
        return False

    def update(self):
        super().update()
        self.maybe_hit_player()
        
        vy = 700                                          # Vertical velocity
        if self.jump(vy):
            player_pos = self.game.player.rect.center
            dx = player_pos[0] - self.x                   # Δx (signed distance)
            g = self.gravity
            vx = clamp((dx * g) / (2.0 * vy), -250, 250)  # Horizontal velocity (calculated)
            self.speed[0] = vx

    def hit_by(self, sprite):
        cur_time = time()
        if self.hit_at is not None and cur_time - self.hit_at < GRACE_PERIOD:
            return
        particle_explosion(
            game=self.game,
            image='enemy_hit_particle.png',
            pos=self.rect.center,
            min_speed=30,
            max_speed=50,
            min_lifespan=0.3,
            max_lifespan=0.8,
            count=5
        )
        self.hit_at = cur_time
        self.health -= 1
        if self.health <= 0:
            self.die()
            return

        vx = sign_choose(sprite.rect.center[0] - self.rect.center[0], -200, rd.choice([-200, 200]), 200)
        self.speed = [vx, -500.0]

    def die(self):
        super().die()
        self.loot()
        particle_explosion(
            game=self.game,
            image='enemy_death_particle.png',
            pos=self.rect.center,
            min_speed=50,
            max_speed=70,
            min_lifespan=0.5,
            max_lifespan=0.8,
            count=10
        )

    def loot(self):
        self.loot_health(rd.randint(1, 3))

    def loot_health(self, hp):
        self.game.player.health = min(self.game.player.health + hp, 10)
