import pygame

from src import constants
from src.character import Character
from src.camera import Camera


class App:
    def init(self):
        self.objects = []

        character = Character((150, 50))
        self.objects.append(character)

        pygame.init()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGH))
        pygame.display.set_caption("Agar.io clone")

        Camera.followed_character = character

    def run(self):
        self.running = True

        while self.running:
            self.update()
            self.draw()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        for object in self.objects:
            object.update()

        Camera.update()

    def draw(self):
        self.screen.fill(constants.SCREEN_BACKGROUND_COLOR)

        for object in self.objects:
            object.draw(self.screen)

        pygame.display.flip()
