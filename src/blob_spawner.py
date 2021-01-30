import pygame

from src import constants
from src.character import Character
from src.blob import Blob

import random
from math import sin, cos


class BlobSpawner:
    def __init__(self):
        self.last_spawn = pygame.time.get_ticks()

    def spawn_blob(self, app):
        x = random.uniform(0, constants.FIELD_WIDTH)
        y = random.uniform(0, constants.FIELD_HEIGHT)
        app.objects.append(Blob((x, y)))
        app.blob_count += 1

    def update(self, app):
        current_time = pygame.time.get_ticks()

        if self.last_spawn + constants.BLOB_SPAWNER_COOLDOWN <= current_time:
            for _ in range(0, constants.BLOB_SPAWNER_MAX_PER_TICK):
                if app.blob_count >= constants.BLOB_SPAWNER_UPPER_LIMIT:
                    break

                self.spawn_blob(app)

            self.last_spawn = current_time
