from vpython import *

from Simulation import Simulation
from CollisionsDetection import *
from CollisionsEffects import *

from VObjects.VBox import VBox
from VObjects.VWall import VWall

import Utility

simulation = Simulation(dt = 0.00001, t_end = 4, rate = 10000, scene_size_x = 1920, scene_size_y = 1080)
simulation.scene.range = 1

k = 3   # used to compute mass of one of the boxes.  It is directly linked to number
        # of digits in computed value of Pi
boxes = [VBox(pos = vec(-0.25, 0.05, 0), vel=vec(1, 0, 0), size = vec(0.1, 0.1, 0.1), mass = 100 ** k, color=Utility.randomColor(), make_trail = False),
         VBox(pos = vec(0, 0.05, 0), size = vec(0.1, 0.1, 0.1), mass = 1, color=Utility.randomColor(), make_trail = False)]
simulation.track_objects(boxes)

walls = [VWall(pos = vec(0.5 + 1, 0, 0), size = vec(1, 2, 1)),
         VWall(pos = vec(-100 + 1, -0.5, 0), size = vec(200, 1, 1))]
simulation.track_objects(walls)

# define how to detect collision between objects used in simulation and what
# should happen on collision
simulation.collider.add_collision_rule((VBox, VBox), colliding_boxes, simple_collision)
simulation.collider.add_collision_rule((VBox, VWall), colliding_boxes, flip_x)
simulation.collider.add_collision_rule((VWall, VWall), None, None)

t_label = label(pos = vec(1, 0.8, 0))
hits_label = label(pos = vec(1, 0.7, 0))

def aft_update():
    hits_label.text = str(round(simulation.collider.counter, 2))
    t_label.text = str(round(simulation.t, 2))

simulation.after_update = aft_update    # use defined hook to add custom behavior
simulation.run()