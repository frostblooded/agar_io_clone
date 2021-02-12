from src import constants
from src.character import Character
from src.helpers import Helpers
from src.controllers.player_controller import PlayerController

import pygame


class CharacterSpawner:
    def __init__(self):
        self.last_spawn = pygame.time.get_ticks()
        self.ai_spawned = 0

    def spawn_starting_ai(self, app):
        # - 1 because we spawn the player character separately
        for _ in range(0, constants.CHARACTER_SPAWNER_MAX_CHARACTERS):
            app.objects.append(
                Character(Helpers.get_random_pos(), "AI {}".format(self.ai_spawned), app.ai_controllers.pop()))
            self.ai_spawned += 1

    def spawn_starting_player(self, app):
        return Character(Helpers.get_random_pos(), "Player", PlayerController())

    def update(self, app):
        current_time = pygame.time.get_ticks()

        if self.last_spawn + constants.CHARACTER_SPAWNER_COOLDOWN <= current_time:
            character_count = 0

            for obj in app.objects:
                if type(obj) is Character:
                    character_count += 1

            if character_count < constants.CHARACTER_SPAWNER_MAX_CHARACTERS:
                print("SPAWNING NEW AI")
                app.objects.append(
                    Character(Helpers.get_random_pos(), "AI {}".format(self.ai_spawned), app.ai_controllers.pop()))
                self.ai_spawned += 1
                self.last_spawn = pygame.time.get_ticks()
