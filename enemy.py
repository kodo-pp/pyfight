import random as rd
from time import time

from falling_sprite import FallingSprite
from load_image import load_image
from clamp import clamp
from sign_choose import sign_choose
from particle_explosion import particle_explosion
from config import *

class Enemy(FallingSprite):
    def __init__(self, image, health, **kwargs):
        super().__init__(**kwargs)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.speed = [0, 0]
        self.hit_at = None
        self.health = health

    def maybe_hit_player(self):
        if self.rect.colliderect(self.game.player1.rect):
            self.game.player1.hit_by(self)
            return True
        if self.rect.colliderect(self.game.player2.rect):
            self.game.player2.hit_by(self)
            return True
        return False

    def update(self):
        super().update()
        self.maybe_hit_player()
        player = self.game.get_nearest_player(self.rect.center)
        
        vy = ENEMY_JUMP_SPEED                             # Vertical velocity
        if self.jump(vy):
            player_pos = player.rect.center
            dx = player_pos[0] - self.x                   # Δx (signed distance)
            g = self.gravity
            vx = clamp((dx * g) / (2.0 * vy), -ENEMY_MAX_SPEED, ENEMY_MAX_SPEED)
            self.speed[0] = vx

    def hit_by(self, sprite):
        cur_time = time()
        if self.hit_at is not None and cur_time - self.hit_at < ENEMY_GRACE_PERIOD:
            return
        particle_explosion(
            game=self.game,
            image='enemy_hit_particle.png',
            pos=self.rect.center,
            min_speed=ENEMY_HIT_PARTICLE_MIN_SPEED,
            max_speed=ENEMY_HIT_PARTICLE_MAX_SPEED,
            min_lifespan=ENEMY_HIT_PARTICLE_MIN_LIFETIME,
            max_lifespan=ENEMY_HIT_PARTICLE_MAX_LIFETIME,
            count=ENEMY_HIT_PARTICLE_COUNT
        )
        self.hit_at = cur_time
        self.health -= 1
        if self.health <= 0:
            self.die()
            return

        vx = sign_choose(
            sprite.rect.center[0] - self.rect.center[0],
            -ENEMY_MAX_SPEED,
            rd.choice([-ENEMY_MAX_SPEED, ENEMY_MAX_SPEED]),
            ENEMY_MAX_SPEED
        )
        self.speed = [vx, -ENEMY_JUMP_SPEED]

    def die(self):
        super().die()
        self.loot()
        particle_explosion(
            game=self.game,
            image='enemy_death_particle.png',
            pos=self.rect.center,
            min_speed=ENEMY_DEATH_PARTICLE_MIN_SPEED,
            max_speed=ENEMY_DEATH_PARTICLE_MAX_SPEED,
            min_lifespan=ENEMY_DEATH_PARTICLE_MIN_LIFETIME,
            max_lifespan=ENEMY_DEATH_PARTICLE_MAX_LIFETIME,
            count=ENEMY_DEATH_PARTICLE_COUNT
        )

    def loot(self):
        self.loot_health(rd.randint(1, 3))
        self.game.score += 1

    def loot_health(self, hp):
        player = self.game.get_random_player()
        player.health = min(player.health + hp, PLAYER_MAX_HEALTH)
