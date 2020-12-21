import pygame

from src import constants
from src.character import Character
from src.blob import Blob

import random
from math import sin, cos


class BlobSpawner:
    def __init__(self):
        self.last_spawn = pygame.time.get_ticks()

    def spawn(self, objects):
        for obj in objects:
            if type(obj) is Character:
                self.spawn_blob_near(objects, obj)

    def spawn_blob_near(self, objects, character):
        min_val = character.size + constants.BLOB_SPAWNER_RADIUS_MIN_ZONE
        max_val = min_val + constants.BLOB_SPAWNER_RADIUS_VARIANCE
        radius = random.uniform(min_val, max_val)
        angle = random.uniform(0, 360)
        offset = (cos(angle) * radius, sin(angle) * radius)
        objects.append(Blob(character.position + offset))

    def update(self, objects):
        current_time = pygame.time.get_ticks()

        if self.last_spawn + constants.BLOB_SPAWNER_COOLDOWN <= current_time:
            self.spawn(objects)
            self.last_spawn = current_time
