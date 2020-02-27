from vpython import *
import math
import itertools
import random

from SystemQuantities import SystemQuantities

from CollisionsDetection import *
from CollisionsEffects import *
from Collider import Collider

from VObjects.VBall import VBall
from VObjects.VWall import VWall

import Utility

def generateBox(center, inside_width, inside_length, wall_width, col=color.magenta):
    return [VWall(center + vec(-inside_width / 2, 0, 0), vec(wall_width, inside_length + wall_width, wall_width), color = col),
         VWall(center + vec(inside_width / 2, 0, 0), vec(wall_width, inside_length + wall_width, wall_width), color = col),
         VWall(center + vec(0, -inside_length / 2, 0), vec(inside_width + wall_width, wall_width, wall_width), color = col),
         VWall(center + vec(0,  inside_length / 2, 0), vec(inside_width + wall_width, wall_width, wall_width), color = col)]

def generateVBalls(ballsCount, left_top_corner, right_down_corner, min_vel, max_vel, radius, mass):
    balls = []

    while len(balls) < ballsCount:
        position = vec(random.uniform(left_top_corner.x, right_down_corner.x), random.uniform(right_down_corner.y, left_top_corner.y), 0)
        velocity = vec(random.uniform(min_vel, max_vel), random.uniform(min_vel, max_vel), 0)

        is_colliding = False
        for ball in balls:
            if mag(ball.obj.pos - position) < 3 * radius:   #2 radii are enough to determine collision, but little additional space make
                                                            #distribution nicer
                is_colliding = True
                break

        if not is_colliding:
            balls.append(VBall(pos = position, radius = radius, mass = mass, vel = velocity, col = Utility.randomColor(), make_trail = False))

    return balls

dt = 0.01
t_end = 30

balls_count = 40
min_vel = -20
max_vel = 20
radius = 1
mass = 1

scene = canvas()
scene.width = 1000
scene.height = 1000

wall_width = 2
empty_space_width = 40
empty_space_length = 60
max_width_to_spawn = (empty_space_width - wall_width - 2 * radius) / 2 - 3
max_length_to_spawn = (empty_space_length - wall_width - 2 * radius) / 2 - 3

collider = Collider()
collider.add_collision_rule((VBall, VBall), colliding_balls, elastic_collision_balls_2d)
collider.add_collision_rule((VBall, VWall), colliding_ball_wall, conserved_energy_collision_ball_wall)

system_quantities = SystemQuantities()

balls = generateVBalls(balls_count, vec(-max_width_to_spawn, max_length_to_spawn, 0), vec(max_width_to_spawn, -max_length_to_spawn, 0), min_vel, max_vel, radius, mass)
walls = generateBox(vec(0,0,0), empty_space_width, empty_space_length, wall_width)

t = 0
t_label = label(pos = vec(empty_space_width / 2, empty_space_length / 2, 0), text=str(round(t, 2)))

while t < t_end:
    rate(100)

    t += dt
    t_label.text = str(round(t, 2))

    system_quantities.compute(balls, "momentum", "global", True)
    system_quantities.compute(balls, "kinetic energy", "global", True)

    for ball in balls: ball.update(dt)
    
    collider.apply_to_combinations(balls, 2)
    collider.apply_to_product(balls, walls)

system_quantities.plot(["momentum", "kinetic energy"], ["global"])