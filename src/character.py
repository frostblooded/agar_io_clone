import pygame
from pygame.math import Vector2


from src import constants
from src.controllers.player_controller import PlayerController
from src.painter import Painter


class Character:
    def __init__(self, position):
        self.position = Vector2(position)
        self.size = constants.CHARACTER_STARTING_SIZE
        self.speed = constants.CHARACTER_STARTING_SPEED
        self.controller = PlayerController(self)

    def update(self):
        self.controller.update()

    def draw(self, screen):
        Painter.draw_circle(screen, (255, 0, 0), self.position, self.size)
