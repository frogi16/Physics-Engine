from VObjects.VObject import VObject

from Segment import Segment

from vpython import box
from vpython import color
from vpython import vec

import math

class VWall(VObject):
    """Complete physical and graphical representation of wall - stationary rectangle aligned with X and Y axis"""

    @staticmethod
    def class_id():
        return "VWall"

    def __init__(self, pos, size=vec(1, 1, 1), color=color.white):
        super().__init__(pos, math.inf, vec(0, 0, 0))

        self.obj = box(pos = pos, size = size, color = color)
        self.segment_top = Segment(vec(pos.x - size.x / 2, pos.y - size.y / 2, 0), vec(pos.x + size.x / 2, pos.y - size.y / 2, 0))
        self.segment_down = Segment(vec(pos.x - size.x / 2, pos.y + size.y / 2, 0), vec(pos.x + size.x / 2, pos.y + size.y / 2, 0))
        self.segment_right = Segment(vec(pos.x + size.x / 2, pos.y - size.y / 2, 0), vec(pos.x + size.x / 2, pos.y + size.y / 2, 0))
        self.segment_left = Segment(vec(pos.x - size.x / 2, pos.y - size.y / 2, 0), vec(pos.x - size.x / 2, pos.y + size.y / 2, 0))

        self.stationary = True

    def update(self, dt):
        None

    def apply_force(self, force):
        None

    def apply_acceleration(self, accel):
        None