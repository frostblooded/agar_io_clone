from pygame import draw

from src.camera import Camera


class Painter:
    def draw_circle(screen, color, position, radius):
        moved_position = position - Camera.position
        draw.circle(screen, (255, 0, 0), moved_position, radius)
