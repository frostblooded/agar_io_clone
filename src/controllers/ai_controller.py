import pygame
from pygame.math import Vector2

from src import constants
from src.blob import Blob

import sys


class AIController:
    def __init__(self, character):
        self.character = character

    def find_closest_blob(self, objects):
        closest_blob = None
        closest_dist = sys.float_info.max

        for obj in objects:
            if type(obj) is Blob:
                distance = (obj.position - self.character.position).length()

                if distance < closest_dist:
                    closest_dist = distance
                    closest_blob = obj

        return closest_blob

    def update(self, app):
        closest_blob = self.find_closest_blob(app.objects)

        if closest_blob is None:
            return

        movement = (closest_blob.position -
                    self.character.position).normalize()
        self.character.position += movement * self.character.get_speed()
