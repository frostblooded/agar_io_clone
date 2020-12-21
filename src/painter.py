import pygame
from pygame.math import Vector2

from src.camera import Camera
from src import constants


class Painter:
    def draw_circle(screen, color, position, radius):
        zoomed_position = position * Camera.zoom
        zoomed_radius = radius * Camera.zoom
        zoomed_camera_position = Camera.position * Camera.zoom

        moved_position = zoomed_position - zoomed_camera_position + \
            Vector2(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
        pygame.draw.circle(screen, (255, 0, 0), moved_position, zoomed_radius)

    def draw_background(screen, background_image):
        screen.blit(background_image, -Camera.position)
