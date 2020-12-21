import pygame
from pygame.math import Vector2

from src import constants


class PlayerController:
    def __init__(self, character):
        self.character = character

    def update(self):
        field_center = (constants.SCREEN_WIDTH / 2,
                        constants.SCREEN_HEIGHT / 2)
        movement = (Vector2(pygame.mouse.get_pos()) - field_center).normalize()
        self.character.position += movement * self.character.speed
