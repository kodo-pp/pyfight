MAX_SPEED = 300.0
JUMP_SPEED = 700.0
SPEED_INCREMENT = 50.0

AIR_RESISTANCE = 0.01
FRICTION = 0.15

MAX_HEALTH = 10
GRACE_PERIOD = 0.4

LASER_COOLDOWN = 0.1

import random as rd
from time import time

from falling_sprite import FallingSprite
from load_image import load_image
from clamp import clamp
from sign_choose import sign_choose
from game_over import GameOver
from laser import Laser

class Player(FallingSprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_image = load_image('player.png')
        self.hit_image = load_image('player_hit.png')
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.speed = [0.0, 0.0]
        self.health = MAX_HEALTH
        self.hit_at = None
        self.is_hit = False
        self.locked = False
        self.last_shot = None

    def go_left(self):
        if self.locked:
            return
        self.speed[0] -= SPEED_INCREMENT
        self.clamp_speed()

    def go_right(self):
        if self.locked:
            return
        self.speed[0] += SPEED_INCREMENT
        self.clamp_speed()

    def clamp_speed(self):
        self.speed[0] = clamp(self.speed[0], -MAX_SPEED, MAX_SPEED)

    def jump(self):
        if self.locked:
            return False
        if self.maybe_wall_jump():
            return True
        return super().jump(JUMP_SPEED)

    def update(self):
        super().update()
        is_hit = self.hit_at is not None and time() - self.hit_at < GRACE_PERIOD
        if self.is_hit != is_hit:
            self.is_hit = is_hit
            if is_hit:
                self.image = self.hit_image
            else:
                self.image = self.base_image
        if self.is_on_ground():
            self.locked = False
            self.speed[0] *= (1.0 - FRICTION)
        else:
            self.speed[0] *= (1.0 - AIR_RESISTANCE)

    def maybe_wall_jump(self):
        if self.hits_right_wall():
            self.speed = [-MAX_SPEED, -JUMP_SPEED]
            self.locked = True
            return True
        if self.hits_left_wall():
            self.speed = [MAX_SPEED, -JUMP_SPEED]
            self.locked = True
            return True
        return False

    def hit_by(self, enemy):
        cur_time = time()
        if self.hit_at is not None and cur_time - self.hit_at < GRACE_PERIOD:
            return
        self.hit_at = cur_time
        self.health -= 1
        if self.health <= 0:
            raise GameOver()

        vx = sign_choose(enemy.rect.center[0] - self.rect.center[0], -200, rd.choice([-200, 200]), 200)
        self.locked = True
        self.speed = [vx, -500.0] 

    def shoot(self):
        speed = [sign_choose(self.speed[0], 1000, None, -1000), 0]
        if speed[0] is None:
            return False
        laser = Laser(self.game, speed, self.rect.center)
        self.game.add_sprite(laser)
        return True
    
    def maybe_shoot(self):
        cur_time = time()
        if self.last_shot is None:
            self.last_shot = cur_time
            return self.shoot()

        if cur_time - self.last_shot < LASER_COOLDOWN:
            return False
        self.last_shot = cur_time
        self.shoot()
        return True
        
        
