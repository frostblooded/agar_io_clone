import pygame
from pygame.math import Vector2


from src import constants


class Character:
    def __init__(self, position):
        self.position = Vector2(position)
        self.size = constants.CHARACTER_STARTING_SIZE
        self.speed = constants.CHARACTER_STARTING_SPEED

    def update(self):
        mouse_pos = Vector2(pygame.mouse.get_pos())
        movement = (mouse_pos - self.position).normalize()
        self.position += movement * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.size)
