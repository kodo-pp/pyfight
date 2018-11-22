from falling_sprite import FallingSprite
from load_image import load_image


class Enemy(FallingSprite):
    def __init__(self, game, image, gravity):
        super().__init__(game, gravity)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.speed = [300, 0]

    def update(self):
        super().update()
        self.jump(700)
