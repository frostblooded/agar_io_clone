import random

from src import constants


class Helpers:
    @staticmethod
    def get_random_pos():
        x = random.uniform(0, constants.SCREEN_WIDTH)
        y = random.uniform(0, constants.SCREEN_HEIGHT)
        return (x, y)
