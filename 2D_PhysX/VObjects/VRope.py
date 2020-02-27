from VObjects.VObject import VObject

from vpython import sphere
from vpython import color
from vpython import vec
from vpython import cylinder
from vpython import dot
from vpython import norm

from Utility import perp_product

class VRope(VObject):
    """Complete physical and graphical representation of a rope"""

    @staticmethod
    def class_id():
        return "VRope"

    def __init__(self, connected_objects, hook_points=None, radius=0.1, col=color.white):
        if len(connected_objects) != 2:
            raise ValueError("connected_objects needs to be two elements long.")

        super().__init__(connected_objects[0].obj.pos, 0, vec(0, 0, 0))

        self.connected_objects = connected_objects
        self.obj = cylinder(pos = connected_objects[0].obj.pos, axis= connected_objects[1].obj.pos - connected_objects[0].obj.pos, radius = radius, color=col)
        self.hook_points = hook_points

    def __del__(self):
        del self.connected_objects
        del self.hook_points

    def update(self, dt):
        if self.hook_points:
            self.obj.axis = self.connected_objects[1].to_global(self.hook_points[1]) - self.connected_objects[0].to_global(self.hook_points[0])
            frc = dot(self.connected_objects[0].force, norm(self.obj.axis)) * norm(self.obj.axis)
            self.connected_objects[0].apply_force(frc, self.connected_objects[0].to_global(self.hook_points[0]))
            frc = dot(self.connected_objects[1].force, norm(-self.obj.axis)) * norm(self.obj.axis)
            self.connected_objects[1].apply_force(frc, self.connected_objects[1].to_global(self.hook_points[1]))
        else:
            self.obj.axis = self.connected_objects[1].obj.pos - self.connected_objects[0].obj.pos
            self.connected_objects[0].apply_force(dot(self.connected_objects[0].force, norm(self.obj.axis)) * norm(self.obj.axis))
            self.connected_objects[1].apply_force(dot(self.connected_objects[0].force, norm(-self.obj.axis)) * norm(self.obj.axis))

        self.circular_buffer.push(self.obj.pos)

        if self.hook_points:
            self.obj.pos = self.connected_objects[0].to_global(self.hook_points[0])
        else:
            self.obj.pos = self.connected_objects[0].obj.pos
        
    def apply_force(self, force):
        None
        
    def apply_acceleration(self, accel):
        None