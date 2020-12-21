class Collider:
    def handle_collisions(objects):
        # This quadratic collision checker might get slow if
        # there are a lot of things on the playing field.
        # TODO: Store objects in a KD tree so that collision checking
        # becomes much faster.
        for object in objects:
            for other_object in objects:
                if object != other_object:
                    if object.get_collides_with(other_object):
                        object.collide(other_object)
                        other_object.collide(object)
