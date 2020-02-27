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

from VObjects.VBox import VBox
from VObjects.VPoint import VPoint
from VObjects.VSpring import VSpring
from VObjects.VRope import VRope

import Utility

dt = 0.001
t_end = 200

scene = canvas()
scene.width = 1920
scene.height = 1000

system_quantities = SystemQuantities()
system_quantities.addQuantity("gravitational potential energy",  "J",    Reductor(0, operator.add),   lambda vObj : vObj.mass * 9.81 * vObj.obj.pos.y)

box = VBox(vec(-5, -20, 0), mass = 10, size=vec(10, 2, 2), color=color.red)
hinge = VPoint(vec(-20, 0, 0))
spring = VSpring([hinge, box], 10, [vec(0, 0, 0), vec(-5, 0, 0)])
hinge2 = VPoint(vec(20, 0, 0))
spring2 = VSpring([hinge2, box], 10, [vec(0, 0, 0), vec(5, 0, 0)])

t = 0
tlabel = label(pos = vec(1, 1, 0), text = str(t))
energy_label = label(pos = vec(30, 50, 0))

while t < t_end:
    rate(1000)

    t += dt
    tlabel.text = str(round(t, 2))

    box.apply_force(9.81 * vec(0, -1, 0) * box.mass)

    spring.update(dt)
    spring2.update(dt)
    hinge.update(dt)
    hinge2.update(dt)
    box.update(dt)

    kin_energy = system_quantities.compute([box], "kinetic energy", "box", True)
    energy_str = "Kinetic energy: " + str(kin_energy) + "\n"
    
    rot_kin_energy = system_quantities.compute([box], "rotational kinetic energy", "box", True)
    energy_str += "Rotational kinetic energy: " + str(rot_kin_energy) + "\n"

    #elas_energy = system_quantities.compute([spring], "elastic potential
    #energy", "springs", True)
    #energy_str += "Elastic energy: " + str(elas_energy) + "\n"

    grav_energy = system_quantities.compute([box], "gravitational potential energy", "box", True)
    energy_str += "Potential energy: " + str(grav_energy) + "\n"
    
    energy_str += "Sum: " + str(round(kin_energy + rot_kin_energy + grav_energy, 2)) + "\n"

    energy_label.text = energy_str