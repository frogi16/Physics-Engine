import math

from vpython import vec

from vpython import mag
from vpython import proj

from VObjects.VBall import VBall
from VObjects.VWall import VWall

from copy import *

def elastic_collision_balls_2d(vBall1, vBall2, is_colliding):
    if not is_colliding:
        return

    dPos = vBall1.obj.pos - vBall2.obj.pos
    collision_angle = math.atan2(dPos.y,dPos.x)

    vel1 = mag(vBall1.vel)
    vel2 = mag(vBall2.vel)

    direction_1 = math.atan2(vBall1.vel.y, vBall1.vel.x)
    direction_2 = math.atan2(vBall2.vel.y, vBall2.vel.x)

    new_xspeed_1 = vel1 * math.cos(direction_1 - collision_angle)
    new_xspeed_2 = vel2 * math.cos(direction_2 - collision_angle)
    
    final_xspeed_1 = ((vBall1.mass - vBall2.mass) * new_xspeed_1 + (vBall2.mass + vBall2.mass) * new_xspeed_2) / (vBall1.mass + vBall2.mass)
    final_xspeed_2 = ((vBall1.mass + vBall1.mass) * new_xspeed_1 + (vBall2.mass - vBall1.mass) * new_xspeed_2) / (vBall1.mass + vBall2.mass)
    
    final_yspeed_1 = vel1 * math.sin(direction_1 - collision_angle)
    final_yspeed_2 = vel2 * math.sin(direction_2 - collision_angle)

    vBall1.vel.x = math.cos(collision_angle) * final_xspeed_1 + math.cos(collision_angle + math.pi / 2) * final_yspeed_1
    vBall1.vel.y = math.sin(collision_angle) * final_xspeed_1 + math.sin(collision_angle + math.pi / 2) * final_yspeed_1
    vBall2.vel.x = math.cos(collision_angle) * final_xspeed_2 + math.cos(collision_angle + math.pi / 2) * final_yspeed_2
    vBall2.vel.y = math.sin(collision_angle) * final_xspeed_2 + math.sin(collision_angle + math.pi / 2) * final_yspeed_2

    vBall1.reverseUpdate()
    vBall2.reverseUpdate()

def conserved_energy_collision_ball_wall(vBall, vWall, axis):
    if axis == "x":
        vBall.vel.x *= -1
    elif axis == "y":
        vBall.vel.y *= -1

def simple_collision(vObj1, vObj2, is_colliding):
    if not is_colliding:
        return

    v1 = vObj1.vel
    v2 = vObj2.vel

    m1 = vObj1.mass
    m2 = vObj2.mass

    vObj1.vel, vObj2.vel = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2), (2 * m1 * v1 + (m2 - m1) * v2) / (m1 + m2)

def flip_x(vObj1, vObj2, is_colliding):
    if not is_colliding:
        return

    vObj1.vel.x *= (-1)