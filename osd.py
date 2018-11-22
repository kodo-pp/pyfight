from pygame.sprite import Sprite


class OSD(Sprite):
    def __init__(self, game, pos):
        super().__init__()
        self.game = game
        self.pos = pos
