from falling_sprite import FallingSprite
from load_image import load_image
from clamp import clamp


class Enemy(FallingSprite):
    def __init__(self, image, **kwargs):
        super().__init__(**kwargs)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.speed = [0, 0]

    def maybe_hit_player(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.player.hit_by(self)
            return True
        return False

    def update(self):
        super().update()
        self.maybe_hit_player()
        
        vy = 700                                          # Vertical velocity
        if self.jump(vy):
            player_pos = self.game.player.rect.center
            dx = player_pos[0] - self.x                   # Δx (signed distance)
            g = self.gravity
    
            vx = clamp((dx * g) / (2.0 * vy), -250, 250)  # Horizontal velocity (calculated)
    
            self.speed[0] = vx
