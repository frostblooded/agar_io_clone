import pygame
from pygame.math import Vector2

from src import constants


class PlayerController:
    def __init__(self, character):
        self.character = character

    def update(self, app):
        field_center = (constants.SCREEN_WIDTH / 2,
                        constants.SCREEN_HEIGHT / 2)
        movement_dir = Vector2(pygame.mouse.get_pos()) - field_center

        if movement_dir.length() == 0:
            return

        movement = movement_dir.normalize()
        self.character.position += movement * self.character.speed
