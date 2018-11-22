from osd import OSD
from load_image import load_image
from pygame import Surface
from pygame.sprite import Group
from player import MAX_HEALTH

class Heart(OSD):
    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.image = load_image('heart_36x36.png')
        self.num = num
        self.rect = self.image.get_rect()
        pos = (36 * num, 0)
        self.rect.x, self.rect.y = pos

    def set_full(self, is_full):
        self.image = load_image('heart_36x36.png' if is_full else 'heart_36x36_empty.png')
        self.rect = self.image.get_rect()
        pos = (36 * self.num, 0)
        self.rect.x, self.rect.y = pos


class HealthOSD(OSD):
    def __init__(self, pos, **kwargs):
        super().__init__(pos=pos, **kwargs)
        self.image = Surface((36 * MAX_HEALTH, 36))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hearts = Group()
        for i in range(MAX_HEALTH):
            self.hearts.add(Heart(i, pos=[-1, -1], **kwargs))
        self.last_health = -1

    def update(self):
        health = self.game.player.health
        if health == self.last_health:
            return
        self.last_health = health
        for heart in self.hearts.sprites():
            heart.set_full(heart.num <= health - 1)
        self.image.fill((0, 0, 0, 0))
        self.hearts.draw(self.image)
