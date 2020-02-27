from VObjects.VObject import VObject

from vpython import box
from vpython import color
from vpython import vec
from vpython import arrow

from vpython import attach_arrow

class VBox(VObject):
    """Complete physical and graphical representation of a box"""

    @staticmethod
    def class_id():
        return "VBox"

    def __init__(self, pos, mass=1, vel=vec(0, 0, 0), rot=0, ang_vel=0, size=vec(1, 1, 1), color=color.white, make_trail=True):
        super().__init__(pos, mass, vel, rot, ang_vel)
        
        self.obj = box(pos = pos, size = size, color=color, make_trail = make_trail)