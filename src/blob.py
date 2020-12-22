from src import constants
from src.painter import Painter

from pygame.math import Vector2


class Blob:
    def __init__(self, position):
        self.position = Vector2(position)
        self.should_die = False
        self.size = constants.BLOB_SIZE
        self.color = Painter.get_random_color()

    def update(self, app):
        pass

    def draw(self, app):
        Painter.draw_circle(app.screen, self.color, self.position, self.size)

    def get_collides_with(self, other_object):
        # Let the other party handle the collision
        return False

    def collide(self, other_object):
        # Let the other object do something about the collision
        pass
