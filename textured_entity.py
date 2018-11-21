from entity import Entity
from load_image import load_image

class TexturedEntity(Entity):
    def __init__(self, texture_name):
        super().__init__()
        self.texture = load_image(texture_name)
        self.rect = self.texture.get_rect()

    def draw(self, screen):
        screen.blit(self.texture, self.rect)

    def get_texture(self):
        return self.texture
