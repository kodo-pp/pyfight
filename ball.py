from textured_entity import TexturedEntity

class BallEntity(TexturedEntity):
    def __init__(self, texture_name):
        super().__init__(texture_name)

    def should_bounce(self, size):
        width, height = size
        should_bounce_x = self.rect.left < 0 or self.rect.right > width
        should_bounce_y = self.rect.top < 0 or self.rect.bottom > height
        return should_bounce_x, should_bounce_y

    def bounced_move(self, size, speed):
        self.move(speed)
        bx, by = self.should_bounce(size)
        resulting_speed = [*speed]
        if bx:
            resulting_speed[0] = -resulting_speed[0]
        if by:
            resulting_speed[1] = -resulting_speed[1]
        return resulting_speed
