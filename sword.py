from time import time

from pygame.sprite import Sprite
from pygame.transform import rotate

from load_image import load_image
from enemy import Enemy
from particle_explosion import particle_explosion
from config import *


class Sword(Sprite):
    def __init__(self, game, owner):
        super().__init__()
        self.image = load_image('sword.png')
        self.base_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = owner.rect.center
        self.last_time = time()
        self.dead = False
        self.game = game
        self.owner = owner
        self.hit_enemies()
        self.rotation = 0.0
    

    def update(self):
        #self.hit_enemies()
        cur_time = time()
        delta_time = cur_time - self.last_time
        self.last_time = cur_time
        
        rotation = 360.0 * delta_time / SWORD_LIFETIME
        self.rotation += rotation
        self.image = rotate(self.base_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.owner.rect.center
        if self.rotation >= 360:
            self.die()

    def hit_enemies(self):
        ret = False
        other_player = self.game.player1 if self.owner is self.game.player2 else self.game.player2
        for sprite in self.game.sprites:
            if self.rect.colliderect(sprite.rect) and (isinstance(sprite, Enemy) or sprite is other_player):
                sprite.hit_by(self)
                ret = True
                particle_explosion(
                    game=self.game,
                    image='sword_hit_particle.png',
                    pos=sprite.rect.center,
                    min_speed=SWORD_PARTICLE_MIN_SPEED,
                    max_speed=SWORD_PARTICLE_MAX_SPEED,
                    min_lifespan=SWORD_PARTICLE_MIN_LIFETIME,
                    max_lifespan=SWORD_PARTICLE_MAX_LIFETIME,
                    count=SWORD_PARTICLE_COUNT
                )
        return ret

    def die(self):
        self.dead = True
