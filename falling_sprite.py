from time import time

from pygame.sprite import Sprite


class FallingSprite(Sprite):
    def __init__(self, game, gravity, pos=[0,0]):
        super().__init__()
        self.game = game
        self.gravity = gravity
        self.last_time = None
        self.x, self.y = pos
        self.dead = False

    def fall(self):
        if self.last_time is None:
            self.last_time = time()
            self.rect.center = self.x, self.y
            return
        delta_time = time() - self.last_time
        self.last_time = time()
        delta_x = delta_time * self.speed[0]
        delta_y = self.speed[1] * delta_time + (delta_time ** 2) / 2.0
        delta_speed = delta_time * self.gravity

        self.speed[1] += delta_speed

        # TODO: check for collisions
        if self.rect.bottom + delta_y >= self.game.height:
            delta_y = self.game.height - self.rect.bottom
            self.speed[1] = 0
        if self.rect.left + delta_x < 0:
            delta_x = -self.rect.left
            self.speed[0] = 0
        if self.rect.right + delta_x >= self.game.width:
            delta_x = self.game.width - self.rect.right
            self.speed[0] = 0

        self.x += delta_x
        self.y += delta_y
        self.rect.center = self.x, self.y

    def is_on_ground(self):
        return abs(self.rect.bottom - self.game.height) < 1e-5

    def hits_right_wall(self):
        return abs(self.rect.right - self.game.width) < 1e-5

    def hits_left_wall(self):
        return abs(self.rect.left) < 1e-5

    def jump(self, speed):
        if self.is_on_ground():
            self.speed[1] = -speed
            return True
        return False

    def update(self):
        self.fall()

    def die(self):
        self.dead = True
