import pygame
from pygame.math import Vector2

from src.camera import Camera
from src import constants


class Painter:
    def draw_circle(screen, color, position, radius):
        moved_position = position - Camera.position + \
            Vector2(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGH / 2)
        pygame.draw.circle(screen, (255, 0, 0), moved_position, radius)

    def draw_background(screen, background_image):
        screen.blit(background_image, -Camera.position)
