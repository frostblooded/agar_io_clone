import pygame


from src.blob import Blob
from src.character import Character


class Collider:
    @staticmethod
    def get_blobs_characters(app):
        blobs = []
        characters = []

        for obj in app.objects:
            if type(obj) is Blob:
                blobs.append(obj)
            elif type(obj) is Character:
                characters.append(obj)

        return (blobs, characters)

    @staticmethod
    def handle_collisions(app):
        start_time = pygame.time.get_ticks()
        (blobs, characters) = Collider.get_blobs_characters(app)

        # This quadratic collision checker might get slow if
        # there are a lot of things on the playing field.
        # TODO: Store objects in a KD tree so that collision checking
        # becomes much faster.
        for char in characters:
            for blob in blobs:
                if char.get_collides_with(blob):
                    char.collide(blob, app)

        for char in characters:
            for other_char in characters:
                if char == other_char:
                    continue

                if char.get_collides_with(other_char):
                    char.collide(other_char, app)
                    other_char.collide(char, app)

        print("Collision detection took {} milliseconds".format(
            pygame.time.get_ticks() - start_time))
