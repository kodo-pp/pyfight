from pygame.sprite import Sprite

from load_image import load_image


class Ball(Sprite):
    def __init__(self, speed, image_filename, screen_size):
        super().__init__()
        self.image = load_image(image_filename)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.screen_size = screen_size

    def should_bounce(self, size):
        width, height = size
        should_bounce_x = self.rect.left < 0 or self.rect.right > width
        should_bounce_y = self.rect.top < 0 or self.rect.bottom > height
        return should_bounce_x, should_bounce_y

    def bounced_move(self, size, speed):
        self.rect.x += speed[0]
        self.rect.y += speed[1]
        bx, by = self.should_bounce(size)
        resulting_speed = [*speed]
        if bx:
            resulting_speed[0] = -resulting_speed[0]
        if by:
            resulting_speed[1] = -resulting_speed[1]
        return resulting_speed

    def update(self, *args):
        self.speed = self.bounced_move(self.screen_size, self.speed)
