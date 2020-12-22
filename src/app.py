import pygame

from src import constants
from src.character import Character
from src.blob import Blob
from src.camera import Camera
from src.painter import Painter
from src.blob_spawner import BlobSpawner
from src.collider import Collider
from src.helpers import Helpers


class App:
    def spawn_characters(self):
        # - 1 because we spawn the player character separately
        for i in range(0, constants.CHARACTERS_SPAWN_COUNT - 1):
            pos = Helpers.get_random_pos()
            self.objects.append(Character(pos, "AI {}".format(i)))

    def init(self):
        self.objects = []

        character = Character((150, 50), "Player", True)
        self.objects.append(character)
        self.spawn_characters()

        pygame.init()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Agar.io clone")

        self.background_image = pygame.image.load('images/background.jpg')

        Camera.followed_character = character
        self.blob_spawner = BlobSpawner()
        self.blob_count = 0

        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.clock = pygame.time.Clock()

    def debug_prints(self):
        print("Time since last frame: {}".format(self.clock.tick(60)))
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

    def draw(self):
        self.screen.fill(constants.SCREEN_BACKGROUND_COLOR)
        Painter.draw_background(self.screen, self.background_image)

        for object in self.objects:
            object.draw(self)

        pygame.display.flip()
