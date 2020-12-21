from pygame.math import Vector2


class Camera:
    position = Vector2(0, 0)
    followed_character = None

    def update():
        if Camera.followed_character:
            Camera.position = Camera.followed_character.position
