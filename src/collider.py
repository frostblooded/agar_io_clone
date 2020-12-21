class Collider:
    def handle_collisions(objects):
        for object in objects:
            for other_object in objects:
                if object != other_object:
                    if object.get_collides_with(other_object):
                        object.collide(other_object)
                        other_object.collide(object)
