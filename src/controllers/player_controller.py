import pygame
from pygame.math import Vector2

from src import constants


class PlayerController:
    def on_end_episode(self, app, character):
        pass

    def update(self, app, character, current_state):
        screen_center = (constants.SCREEN_WIDTH / 2,
                         constants.SCREEN_HEIGHT / 2)
        movement_dir = Vector2(pygame.mouse.get_pos()) - screen_center

        if movement_dir.length() == 0:
            return

        movement = movement_dir.normalize()
        character.position += movement * character.get_speed()
