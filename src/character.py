import pygame
from pygame.math import Vector2


from src import constants
from src.controllers.player_controller import PlayerController
from src.painter import Painter
from src.blob import Blob


from math import log


class Character:
    def __init__(self, position, name, controller):
        self.position = Vector2(position)
        self.size = constants.CHARACTER_STARTING_SIZE
        self.name = name
        self.color = Painter.get_random_color()

        self.controller = controller
        self.player_controlled = type(self.controller) is PlayerController

        self.should_die = False
        self.current_reward = 0

    def update(self, app, current_state):
        if self.controller:
            self.controller.update(app, self, current_state)

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
        size_increase = other_object.size * constants.CHARACTER_EAT_SIZE_GAIN_MULTIPLIER
        self.size += size_increase
        other_object.should_die = True

        if not self.player_controlled:
            self.current_reward = size_increase

        if type(other_object) is Blob:
            app.blob_count -= 1
        elif type(other_object) is Character:
            self.size += constants.CHARACTER_EAT_CHARACTER_ADDITIONAL_GAIN
            self.current_reward += constants.CHARACTER_EAT_CHARACTER_ADDITIONAL_GAIN

            if not other_object.player_controlled:
                app.ai_controllers.append(other_object.controller)
                other_object.current_reward = -100

            other_object.controller.on_end_episode(app, self)

    def get_speed(self):
        # A formula to make bigger characters slower
        size_diff = self.size - constants.CHARACTER_STARTING_SIZE
        size_multiplier = 1 / (log(size_diff / 100 + 1) + 1)
        return constants.CHARACTER_STARTING_SPEED * size_multiplier
