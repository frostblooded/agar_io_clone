import pygame

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


class App:
    def init(self):
        self.objects = []
        self.ai_controllers = []

        for i in range(constants.CHARACTER_SPAWNER_MAX_CHARACTERS-1):
            self.ai_controllers.append(AIController())

        self.character_spawner = CharacterSpawner()
        self.character_spawner.spawn_starting_ai(self)

        self.player_character = self.character_spawner.spawn_starting_player(self)
        self.objects.append(self.player_character)

        pygame.init()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Agar.io clone")

        self.background_image = pygame.image.load('images/background.jpg')

        Camera.followed_character = self.player_character
        self.blob_spawner = BlobSpawner()
        self.blob_count = 0

        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.clock = pygame.time.Clock()

    def debug_prints(self):
        print("Time since last frame: {} milliseconds".format(self.clock.tick(60)))
        print("Blobs: {}".format(self.blob_count))

    def run(self):
        self.running = True

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

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        for object in self.objects:
            object.update(self)

        Collider.handle_collisions(self)
        self.objects = self.get_alive_objects()

        Camera.update()

        self.blob_spawner.update(self)

        self.character_spawner.update(self)

    def draw(self):
        self.screen.fill(constants.SCREEN_BACKGROUND_COLOR)
        Painter.draw_background(self.screen, self.background_image)
        Painter.draw_boundaries(self.screen)

        for object in self.objects:
            object.draw(self)

        pygame.display.flip()
