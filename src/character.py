import pygame
from pygame.math import Vector2


from src import constants
from src.controllers.player_controller import PlayerController
from src.painter import Painter


class Character:
    def __init__(self, position, player_controlled=False):
        self.position = Vector2(position)
        self.size = constants.CHARACTER_STARTING_SIZE
        self.speed = constants.CHARACTER_STARTING_SPEED

        if player_controlled:
            self.controller = PlayerController(self)
        else:
            self.controller = None

        self.should_die = False

    def update(self):
        if self.controller:
            self.controller.update()

    def draw(self, screen):
        Painter.draw_circle(screen, (255, 0, 0), self.position, self.size)

    def get_collides_with(self, other_object):
        distance = (self.position - other_object.position).length()
        return distance < self.size + other_object.size

    def collide(self, other_object):
        if self.size == other_object.size:
            return

        if self.size > other_object.size:
            self.size += other_object.size / 2
            other_object.should_die = True
        else:
            other_object.size += self.size / 2
            self.should_die = True
