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
from VObjects.VWall import VWall

import Utility

def thrusters_pos(vBox):
    thrusters = [vBox.to_global(vec(-vBox.obj.width / 2, 0, 0)),
            vBox.to_global(vec(0, 0, 0)),
            vBox.to_global(vec(vBox.obj.width / 2, 0, 0))]
    return thrusters

dt = 0.001
t_end = 200

scene = canvas()
scene.width = 1920
scene.height = 1000

system_quantities = SystemQuantities()

vehicle = VBox(pos=vec(0,0,0), mass = 10, color = Utility.randomColor())

markers = [VBall(pos=vehicle.obj.pos, radius=0.1, col=color.red, make_trail=False),
           VBall(pos=vehicle.obj.pos, radius=0.1, col=color.red, make_trail=False),
           VBall(pos=vehicle.obj.pos, radius=0.1, col=color.red, make_trail=False)]


def keyInput(evt):
    s = evt.key

    if s == 'left':
        vehicle.apply_force_local(force_forward, thrusters[0])
    if s == 'right':
        vehicle.apply_force_local(force_forward, thrusters[2])

scene.bind('keyup', keyInput)

arrows = [arrow(), arrow()]
t = 0
tlabel = label(pos = vec(1, 1, 0), text = str(t))

while t < t_end:
    rate(1000)

    t += dt
    tlabel.text = str(round(t, 2))

    vehicle.update(dt)

    thrusters = thrusters_pos(vehicle)

    for i in range(3):
        markers[i].obj.pos = vec(thrusters[i].x, thrusters[i].y, 0.5)

    k = keysdown() # a list of keys that are down
    
    force_forward = (vehicle.to_global(vec(0, 1, 0)) - vehicle.obj.pos) * 500
    
    arrows[0].pos = vec(thrusters[0].x, thrusters[0].y, 0.5)
    arrows[0].axis = force_forward / 500
    
    arrows[1].pos = vec(thrusters[2].x, thrusters[2].y, 0.5)
    arrows[1].axis = force_forward / 500

    

