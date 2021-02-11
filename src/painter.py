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

    # world space to screen space coordinates
    @staticmethod
    def to_zoomed_camera_pos(pos):
        zoomed_position = pos * Camera.zoom
        zoomed_camera_position = Camera.position * Camera.zoom

        moved_position = zoomed_position - zoomed_camera_position + \
            Vector2(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)

        return moved_position

    @staticmethod
    def draw_background(screen, background_image):
        starting_x = -Camera.position.x * constants.BACKGROUND_SPEED_MULTIPLIER
        starting_y = -Camera.position.y * constants.BACKGROUND_SPEED_MULTIPLIER
        current_x = starting_x
        current_y = starting_y
        (step_x, step_y) = background_image.get_size()

        while current_x < constants.FIELD_WIDTH:
            current_y = starting_y

            while current_y < constants.FIELD_HEIGHT:
                screen.blit(background_image, (current_x, current_y))
                current_y += step_y

            current_x += step_x

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

    @staticmethod
    def draw_line(screen, color, start_pos, end_pos):
        start_pos = Vector2(start_pos)
        end_pos = Vector2(end_pos)
        zoomed_start_pos = Painter.to_zoomed_camera_pos(start_pos)
        zoomed_end_pos = Painter.to_zoomed_camera_pos(end_pos)
        pygame.draw.line(screen, color, zoomed_start_pos, zoomed_end_pos)

    @staticmethod
    def draw_boundaries(screen):
        width = constants.FIELD_WIDTH
        height = constants.FIELD_HEIGHT
        color = (255, 0, 0)
        Painter.draw_line(screen, color,
                          (0, 0), (width, 0))
        Painter.draw_line(screen, color,
                          (0, 0), (0, height))
        Painter.draw_line(screen, color,
                          (0, height), (width, height))
        Painter.draw_line(screen, color,
                          (width, height), (width, 0))
