from vpython import vec

class AttrHolder(object):
    pass

class VPoint(object):
    """Physical representation of point in space"""

    @staticmethod
    def class_id():
        return "VPoint"

    def __init__(self, pos):
        self.obj = AttrHolder()
        self.obj.pos = pos
        self.force = vec(0, 0, 0)
        self.stationary = True

    def update(self, dt):
        None

    def to_local(self, vector):
        return vector - self.obj.pos

    def to_global(self, vector):
        return vector + self.obj.pos

    def apply_force(self, force, point_of_impact=None):
        None

    def apply_force_local(self, force, point_of_impact=None):
        None
        
    def apply_acceleration(self, accel):
        None