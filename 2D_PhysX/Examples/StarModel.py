from vpython import *
import math
import itertools
import random

import Forces

from SystemQuantities import SystemQuantities
from SystemQuantities import Reductor
import operator

from CollisionsDetection import *
from CollisionsEffects import *
from Collider import Collider

from VObjects.VBall import VBall
from VObjects.VBox import VBox
from VObjects.VWall import VWall
from VObjects.VPoint import VPoint

import Utility

dt = 0.0001
t_end = 60

k = 3

scene = canvas()
scene.width = 1000
scene.height = 500

collider = Collider()
collider.add_collision_rule((VBall, VBall), colliding_balls, simple_collision)
collider.add_collision_rule((VBall, VWall), colliding_ball_wall, conserved_energy_collision_ball_wall)

system_quantities = SystemQuantities()
system_quantities.addQuantity("gravitational potential energy",  "J",    Reductor(0, operator.add),   lambda vObj : vObj.mass * 9.81 * vObj.obj.pos.y)

balls = [VBall(pos = vec(0, 1 ,0), radius = 0.1, mass = 10, col=Utility.randomColor(), make_trail = False),
         VBall(pos = vec(0, 1.25,0), radius = 0.1, mass = 1, col=Utility.randomColor(), make_trail = False),
         VBall(pos = vec(0, 1.5 ,0), radius = 0.1, mass = 0.1, col=Utility.randomColor(), make_trail = False)]

pos_plot = gcurve(color=color.cyan)
pos_plot2 = gcurve(color=color.blue)

walls = [VWall(pos = vec(0, -0.5, 0), size = vec(1, 1, 1))]

t = 0
tlabel = label(pos = vec(1, 1, 0), text = str(t))
energy_label = label(pos = vec(1, 1.2, 0))
y_label = label(pos = vec(1, 1.4, 0))

while t < t_end:
    rate(100000)

    t += dt
    tlabel.text = str(round(t, 2))
    energy = 0

    for ball in balls:
        ball.apply_force(9.81 * vec(0, -1, 0) * ball.mass)
        ball.update(dt)

        energy += ball.mass * 9.81 * ball.obj.pos.y + 0.5 * ball.mass * mag(ball.vel) ** 2

    collider.apply_to_combinations(balls, 2)
    collider.apply_to_product(balls, walls)
    
    energy_label.text = str(round(energy, 2))
    y_label.text = str(round(balls[2].obj.pos.y,2))

    pos_plot.plot(t, balls[1].obj.pos.y)
    pos_plot2.plot(t, balls[2].obj.pos.y)

