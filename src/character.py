import pygame
from pygame.math import Vector2


from src import constants
from src.controllers.player_controller import PlayerController
from src.controllers.ai_controller import AIController
from src.painter import Painter
from src.blob import Blob


from math import log


class Character:
    def __init__(self, position, name, player_controlled=False):
        self.position = Vector2(position)
        self.size = constants.CHARACTER_STARTING_SIZE
        self.name = name
        self.color = Painter.get_random_color()

        if player_controlled:
            self.controller = PlayerController(self)
        else:
            self.controller = AIController(self)

        self.should_die = False

    def update(self, app):
        if self.controller:
            self.controller.update(app)

    def draw(self, app):
        Painter.draw_circle(app.screen, self.color, self.position, self.size)
        Painter.draw_text(app, self.name, self.position)

    def get_collides_with(self, other_object):
        if self.should_die or other_object.should_die:
            return False

        distance = (self.position - other_object.position).length()
        return distance < self.size + other_object.size

    def collide(self, other_object, app):
        if self.should_die:
            return

        if self.size == other_object.size:
            return

        if self.size > other_object.size:
            self.eat(other_object, app)
        else:
            other_object.eat(self, app)

    def eat(self, other_object, app):
        self.size += other_object.size * constants.CHARACTER_EAT_SIZE_GAIN_MULTIPLIER
        other_object.should_die = True

        if type(other_object) is Blob:
            app.blob_count -= 1
        elif type(other_object) is Character:
            self.size += constants.CHARACTER_EAT_CHARACTER_ADDITIONAL_GAIN

    def get_speed(self):
        # A formula to make bigger characters slower
        size_diff = self.size - constants.CHARACTER_STARTING_SIZE
        size_multiplier = 1 / (log(size_diff / 100 + 1) + 1)
        return constants.CHARACTER_STARTING_SPEED * size_multiplier
