import pygame
from pygame.math import Vector2

from src.camera import Camera
from src import constants

import random


class Painter:
    @staticmethod
    def get_random_color():
        r = random.uniform(0, 255)
        g = random.uniform(0, 255)
        b = random.uniform(0, 255)
        return (r, g, b)

    @staticmethod
    def to_zoomed_camera_pos(pos):
        zoomed_position = pos * Camera.zoom
        zoomed_camera_position = Camera.position * Camera.zoom

        moved_position = zoomed_position - zoomed_camera_position + \
            Vector2(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)

        return moved_position

    @staticmethod
    def draw_background(screen, background_image):
        screen.blit(background_image, -Camera.position)

    @staticmethod
    def draw_text(app, text, position):
        text_surface = app.font.render(text, False, (0, 0, 0))
        text_rect = text_surface.get_rect()
        zoomed_position = Painter.to_zoomed_camera_pos(position)

        # Center the text based on how big it is
        zoomed_position -= Vector2(text_rect.width / 2, text_rect.height / 2)

        app.screen.blit(text_surface, zoomed_position)

    @staticmethod
    def draw_circle(screen, color, position, radius):
        zoomed_radius = radius * Camera.zoom
        zoomed_position = Painter.to_zoomed_camera_pos(position)
        pygame.draw.circle(screen, color, zoomed_position, zoomed_radius)
