from falling_sprite import FallingSprite
from load_image import load_image
from config import *


class ThrownObject(FallingSprite):
    def __init__(self, pos, speed, **kwargs):
        super().__init__(**kwargs)
        self.x, self.y = pos
        self.speed = speed
        self.image = load_image('thrown_object.png')
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        super().update()
        self.maybe_leave_screen()
        self.maybe_hit_player()

    def maybe_leave_screen(self):
        if self.is_on_ground() or self.hits_wall():
            self.die()

    def maybe_hit_player(self):
        if self.rect.colliderect(self.game.player1.rect):
            self.game.player1.hit_by(self)
            self.die()
            return True
        if self.rect.colliderect(self.game.player2.rect):
            self.game.player2.hit_by(self)
            self.die()
            return True
        return False
        
