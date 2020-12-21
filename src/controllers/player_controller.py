import pygame

from pygame.math import Vector2


class PlayerController:
    def __init__(self, character):
        self.character = character

    def update(self):
        mouse_pos = Vector2(pygame.mouse.get_pos())
        movement = (mouse_pos - self.character.position).normalize()
        self.character.position += movement * self.character.speed
