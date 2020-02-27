from vpython import *
import math
import itertools
import random

from SystemQuantities import SystemQuantities
from SystemQuantities import Reductor
import operator

import Forces

from VObjects.VBall import VBall
from VObjects.VWall import VWall
from VObjects.VPoint import VPoint
from VObjects.VSpring import VSpring

import Utility

def generateBalls(n):
    spacing = 5
    walls = []
    walls.append(VWall(vec(0, 0, 0), vec(1, 5, 1)))
    balls = [VBall(pos = vec(spacing + spacing * i,0,0), col=Utility.randomColor(), make_trail = False) for i in range(n)]
    walls.append(VWall(balls[-1].obj.pos + vec(spacing, 0, 0), vec(1, 5, 1)))

    return walls, balls

def generateSprings(points):
    return [VSpring([points[i], points[i + 1]], k, radius=0.3) for i in range(len(points) - 1)]

dt = 0.001
t_end = 10

k = 18
g = 9.81
drag_coefficient = 0.2
y_spacing = 10
number_of_balls = 31

scene = canvas()
scene.width = 1920
scene.height = 1000

system_quantities = SystemQuantities()
system_quantities.addQuantity("gravitational potential energy",  "J",    Reductor(0, operator.add),   lambda vObj : vObj.mass * 9.81 * vObj.obj.pos.y)

walls, balls = generateBalls(number_of_balls)
balls[0].obj.pos.y = y_spacing
balls[-1].obj.pos.y = -y_spacing

scene.center = (walls[0].obj.pos + walls[1].obj.pos) / 2

points = []
points.append(walls[0])
points += balls
points.append(walls[1])

springs = generateSprings(points)

t = 0
tlabel = label(pos = vec(10, 40, 0), text = str(t))
energy_label = label(pos = vec(30, -50, 0))

while t < t_end:
    rate(400)

    t += dt
    tlabel.text = str(round(t, 2))

    for spring in springs:
        spring.update(dt)

    for ball in balls:
        ball.apply_force(9.81 * vec(0, -1, 0) * ball.mass)
        ball.apply_force(Forces.computeLinearAirResistance(ball, drag_coefficient))
        ball.update(dt)

    kin_energy = system_quantities.compute(balls, "kinetic energy", "balls", True)
    energy_str = "Kinetic energy: " + str(kin_energy) + "\n"
    
    elas_energy = system_quantities.compute(springs, "elastic potential energy", "springs", True)
    energy_str += "Elastic energy: " + str(elas_energy) + "\n"

    grav_energy = system_quantities.compute(balls, "gravitational potential energy", "balls", True)
    energy_str += "Potential energy: " + str(grav_energy) + "\n"
    
    energy_str += "Sum: " + str(round(kin_energy + elas_energy + grav_energy, 2)) + "\n"

    energy_label.text = energy_str

system_quantities.plot(["kinetic energy", "elastic potential energy", "gravitational potential energy"], ["balls", "springs", "balls"])