import pygame

from src import constants
from src.character import Character


class App:
    def init(self):
        self.objects = []
        self.objects.append(Character())

        pygame.init()

        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGH))
        pygame.display.set_caption("Agar.io clone")
        self.screen.fill((255, 255, 255))

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

    def draw(self):
        for object in self.objects:
            object.draw(self.screen)

        pygame.display.flip()
