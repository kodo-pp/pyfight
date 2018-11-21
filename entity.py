from pygame import Rect

class Entity:
    def __init__(self):
        self.rect = Rect(0, 0, 0, 0)

    def draw(self, screen):
        pass

    def move(self, offset):
        self.rect = self.rect.move(offset)

    def get_rect(self):
        return self.rect
