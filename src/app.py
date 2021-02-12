import pygame
import torch

from src import constants
from src.character import Character
from src.blob import Blob
from src.camera import Camera
from src.painter import Painter
from src.blob_spawner import BlobSpawner
from src.collider import Collider
from src.helpers import Helpers
from src.character_spawner import CharacterSpawner
from src.controllers.ai_controller import AIController
from src.ai.env_manager import EnvManager


class App:
    def init(self, ai_controllers=[]):
        self.objects = []
        self.ai_controllers = ai_controllers

        ai_controllers_to_create = constants.CHARACTER_SPAWNER_MAX_CHARACTERS - \
            len(self.ai_controllers)
        for _ in range(ai_controllers_to_create):
            self.ai_controllers.append(AIController())

        self.character_spawner = CharacterSpawner()
        self.character_spawner.spawn_starting_ai(self)

        pygame.init()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Agar.io clone")

        self.background_image = pygame.image.load('images/background.jpg')

        Camera.followed_character = self.get_random_ai_character()
        self.blob_spawner = BlobSpawner()
        self.blob_count = 0

        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.clock = pygame.time.Clock()

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.em = EnvManager(self.device)

    def debug_prints(self):
        print("Time since last frame: {} milliseconds".format(self.clock.tick(60)))
        print("Blobs: {}".format(self.blob_count))

    def run(self):
        self.running = True
        self.episode_start_time = pygame.time.get_ticks()

        while self.running:
            self.debug_prints()
            self.update()
            self.draw()

    def get_alive_objects(self):
        alive_objects = []

        for obj in self.objects:
            if obj.should_die == False:
                alive_objects.append(obj)

        return alive_objects

    def get_random_ai_character(self):
        import random

        ai_characters = []

        for obj in self.objects:
            if type(obj) is Character and not obj.player_controlled:
                ai_characters.append(obj)

        return random.choice(ai_characters)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

        if pygame.time.get_ticks() - self.episode_start_time > 60000:
            for obj in self.objects:
                if type(obj) is Character and not obj.player_controlled:
                    obj.controller.on_end_episode(self, obj)
            self.running = False
            return

        current_state = self.em.get_state(self)

        for object in self.objects:
            object.update(self, current_state)

        Camera.update()

        self.blob_spawner.update(self)

        self.character_spawner.update(self)

        Collider.handle_collisions(self)

        if Camera.followed_character.should_die:
            Camera.followed_character = self.get_random_ai_character()

        self.objects = self.get_alive_objects()

    def draw(self):
        if not self.running:
            return
        self.screen.fill(constants.SCREEN_BACKGROUND_COLOR)
        Painter.draw_background(self.screen, self.background_image)
        Painter.draw_boundaries(self.screen)

        for object in self.objects:
            object.draw(self)

        pygame.display.flip()
