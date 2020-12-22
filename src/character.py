import pygame
from pygame.math import Vector2


from src import constants
from src.controllers.player_controller import PlayerController
from src.controllers.ai_controller import AIController
from src.painter import Painter


from math import log


class Character:
    def __init__(self, position, name, player_controlled=False):
        self.position = Vector2(position)
        self.size = constants.CHARACTER_STARTING_SIZE
        self.name = name

        if player_controlled:
            self.controller = PlayerController(self)
        else:
            self.controller = AIController(self)

        self.should_die = False

    def update(self, app):
        print("Character ({}) speed: {}".format(self.name, self.get_speed()))
        if self.controller:
            self.controller.update(app)

    def draw(self, app):
        Painter.draw_circle(app.screen, (255, 0, 0), self.position, self.size)
        Painter.draw_text(app, self.name, self.position)

    def get_collides_with(self, other_object):
        if self.should_die or other_object.should_die:
            return False

        distance = (self.position - other_object.position).length()
        return distance < self.size + other_object.size

    def collide(self, other_object):
        if self.size == other_object.size:
            return

        if self.size > other_object.size:
            self.eat(other_object)
        else:
            other_object.eat(self)

    def eat(self, other_object):
        self.size += other_object.size / 10
        other_object.should_die = True

    def get_speed(self):
        # A formula to make bigger characters slower
        size_diff = self.size - constants.CHARACTER_STARTING_SIZE
        size_multiplier = 1 / (log(size_diff / 100 + 1) + 1)
        return constants.CHARACTER_STARTING_SPEED * size_multiplier
