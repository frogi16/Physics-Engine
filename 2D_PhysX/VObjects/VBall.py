from VObjects.VObject import VObject

from vpython import sphere
from vpython import color
from vpython import vec

class VBall(VObject):
    """Complete physical and graphical representation of a ball"""

    @staticmethod
    def class_id():
        return "VBall"

    def __init__(self, pos, mass=1, vel=vec(0, 0, 0), rot=0, ang_vel=0, radius=1, col=color.white, make_trail=True, label_text=None, label_offset=vec(0,0,0)):
        super().__init__(pos, mass, vel, rot=rot, ang_vel = ang_vel, label_text=label_text, label_offset=label_offset)
        
        self.obj = sphere(pos = pos, radius = radius, color=col, make_trail = make_trail)