import random

from src import constants
from src.camera import Camera

from pygame.math import Vector2

class Helpers:
    @staticmethod
    def get_random_pos():
        x = random.uniform(0, constants.FIELD_WIDTH)
        y = random.uniform(0, constants.FIELD_HEIGHT)
        return (x, y)

    @staticmethod
    def world_space_to_screen_space(pos):
        zoomed_position = pos * Camera.zoom
        zoomed_camera_position = Camera.position * Camera.zoom

        moved_position = zoomed_position - zoomed_camera_position + \
            Vector2(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)

        return moved_position

