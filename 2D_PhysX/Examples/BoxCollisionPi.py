from vpython import *
import math
import itertools
import random

from SystemQuantities import SystemQuantities
from SystemQuantities import Reductor
import operator

from CollisionsDetection import *
from CollisionsEffects import *
from Collider import Collider

import Forces

from VObjects.VBall import VBall
from VObjects.VBox import VBox
from VObjects.VWall import VWall
from VObjects.VPoint import VPoint

import Utility

dt = 0.00001
t_end = 200

k = 3

scene = canvas()
scene.width = 1920
scene.height = 1000
scene.range = 2

collider = Collider()
collider.add_collision_rule((VBox, VBox), colliding_boxes, simple_collision)
collider.add_collision_rule((VBox, VWall), colliding_boxes, flip_x)

system_quantities = SystemQuantities()

boxes = [VBox(pos = vec(-0.25, 0.05, 0), vel=vec(1, 0, 0), size = vec(0.1, 0.1, 0.1), mass = 100 ** k, color=Utility.randomColor(), make_trail = False),
         VBox(pos = vec(0, 0.05, 0), size = vec(0.1, 0.1, 0.1), mass = 1, color=Utility.randomColor(), make_trail = False)]

#wild_box = VBox(pos=vec(0,3,0), ang_vel=3)
walls = [VWall(pos = vec(0.5 + 1, 0, 0), size = vec(1, 2, 1)),
         VWall(pos = vec(-100 + 1, -0.5, 0), size = vec(200, 1, 1))]

t = 0
tlabel = label(pos = vec(1, 1, 0), text = str(t))
hits_label = label(pos = vec(1, 1.2, 0))
energy_label = label(pos = vec(1, 1.4, 0))

while t < t_end:
    rate(10000)

    t += dt
    tlabel.text = str(round(t, 2))
    hits_label.text = str(round(collider.counter, 2))

    for box in boxes: box.update(dt)
#    wild_box.update(dt)

    collider.apply_to_combinations(boxes, 2)
    collider.apply_to_product(boxes, walls)