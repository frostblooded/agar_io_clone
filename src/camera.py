from src import constants

from pygame.math import Vector2


class Camera:
    position = Vector2(0, 0)
    followed_character = None
    zoom = 1

    def update():
        if Camera.followed_character:
            Camera.position = Camera.followed_character.position
            Camera.zoom = constants.CHARACTER_STARTING_SIZE * 10 / \
                Camera.followed_character.size
