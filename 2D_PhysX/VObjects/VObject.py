from abc import ABC

from vpython import vec
from vpython import label
from vpython import cross
from vpython import mag
from vpython import rotate

from math import sin

from Utility import perp_product

from CircularBuffer import CircularBuffer

class VObject(ABC):
    """Base class representing physical object"""

    def __init__(self, pos, mass, vel, rot=0, ang_vel=0, label_text=None, label_offset=vec(0,0,0)):
        self.pos = pos
        self.mass = mass
        self.force = vec(0, 0, 0)
        self.vel = vel
        
        self.center_of_mass = vec(0, 0, 0)

        self.rot = rot
        self.moment_of_inertia = 1  #TODO
        self.torque = 0
        self.ang_vel = ang_vel
        
        self.obj = None
        self.circular_buffer = CircularBuffer()

        if label_text:
            self.label = label(pos = pos, text=label_text)
            self.label.xoffset, self.label.yoffset = label_offset.x, label_offset.y
        else:
            self.label = None

        self.stationary = False

    def update(self, dt):
        self.circular_buffer.push(self.obj.pos)
        
        acceleration = self.force / self.mass
        self.vel += acceleration * dt
        self.obj.pos += self.vel * dt
        self.force = vec(0, 0, 0)

        angular_acceleration = self.torque / self.moment_of_inertia
        self.ang_vel += angular_acceleration * dt
        self.rot += self.ang_vel * dt
        self.obj.rotate(self.ang_vel * dt, vec(0, 0, 1))
        self.torque = 0

        if self.label:
            self.label.pos = self.obj.pos

    def to_local(self, vector):
        if vector:
            return rotate(vector - self.obj.pos, self.rot)
        else: return vector

    def to_global(self, vector):
        temp = rotate(vector, self.rot)
        return self.obj.pos + rotate(vector, self.rot)

    def apply_force_local(self, force, point_of_impact=None):
        self.force += self.to_global(force)

        if point_of_impact:
            r = point_of_impact - self.center_of_mass
            torque = perp_product(r, force)
            self.torque += torque
            
    def apply_force(self, force, point_of_impact=None):
        self.force += force

        if point_of_impact:
            r = self.to_local(point_of_impact) - self.center_of_mass
            torque = perp_product(r, force)
            self.torque += torque
        
    def reverseUpdate(self):
        previousPos = self.circular_buffer.val()

        if previousPos != None:
            self.obj.pos = previousPos

        self.circular_buffer.pop()
        return previousPos

    def destroy(self):
        self.obj.visible = False