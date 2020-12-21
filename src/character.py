import pygame


class Character:
    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (150, 50), 15)
