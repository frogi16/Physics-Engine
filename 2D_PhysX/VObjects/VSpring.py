from VObjects.VObject import VObject
from VObjects.VBall import VBall

from vpython import helix
from vpython import attach_arrow
from vpython import color
from vpython import vec

class VSpring(VObject):
    """Complete physical and graphical representation of a spring"""

    @staticmethod
    def class_id():
        return "VSpring"

    def __init__(self, connected_objects, stiffness, hook_points=None, radius=1, col=color.white):
        if len(connected_objects) != 2:
            raise ValueError("connected_objects needs to be two elements long.")

        super().__init__(connected_objects[0].obj.pos, 0, vec(0, 0, 0))

        self.connected_objects = connected_objects
        self.stiffness = stiffness
        self.obj = helix(pos = connected_objects[0].obj.pos, axis= connected_objects[1].obj.pos - connected_objects[0].obj.pos, radius = radius, color=col)
        self.hook_points = hook_points

    def __del__(self):
        del self.connected_objects
        del self.stiffness
        del self.hook_points

    def update(self, dt):
        if self.hook_points:
            self.obj.axis = self.connected_objects[1].to_global(self.hook_points[1]) - self.connected_objects[0].to_global(self.hook_points[0])
            self.connected_objects[0].apply_force(self.obj.axis * self.stiffness, self.connected_objects[0].to_global(self.hook_points[0]))
            self.connected_objects[1].apply_force(-self.obj.axis * self.stiffness, self.connected_objects[1].to_global(self.hook_points[1]))
        else:
            self.obj.axis = self.connected_objects[1].obj.pos - self.connected_objects[0].obj.pos
            self.connected_objects[0].apply_force(self.obj.axis * self.stiffness)
            self.connected_objects[1].apply_force(-self.obj.axis * self.stiffness)

        self.circular_buffer.push(self.obj.pos)

        if self.hook_points:
            self.obj.pos = self.connected_objects[0].to_global(self.hook_points[0])
        else:
            self.obj.pos = self.connected_objects[0].obj.pos
        
    def apply_force(self, force):
        None
        
    def apply_acceleration(self, accel):
        None
