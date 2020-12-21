import pygame

from src import constants
from src.character import Character
from src.blob import Blob
from src.camera import Camera
from src.painter import Painter
from src.blob_spawner import BlobSpawner
from src.collider import Collider


class App:
    def init(self):
        self.objects = []

        character = Character((150, 50), True)
        self.objects.append(character)
        self.objects.append(Blob((100, 50)))
        self.objects.append(Blob((50, 50)))
        self.objects.append(Blob((0, 50)))
        character.size = 15

        pygame.init()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Agar.io clone")

        self.background_image = pygame.image.load('images/background.jpg')

        Camera.followed_character = character
        self.blob_spawner = BlobSpawner()

    def run(self):
        self.running = True

        while self.running:
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Camera.zoom += 0.5
                elif event.key == pygame.K_DOWN:
                    Camera.zoom -= 0.5
                elif event.key == pygame.K_LEFT:
                    self.objects[0].size += 10
                elif event.key == pygame.K_RIGHT:
                    self.objects[0].size -= 10

        for object in self.objects:
            object.update()

        Collider.handle_collisions(self.objects)
        self.objects = self.get_alive_objects()

        Camera.update()

        self.blob_spawner.update(self.objects)

    def draw(self):
        self.screen.fill(constants.SCREEN_BACKGROUND_COLOR)
        Painter.draw_background(self.screen, self.background_image)

        for object in self.objects:
            object.draw(self.screen)

        pygame.display.flip()
