from vpython import *
import math
import itertools
import copy

import numericalunits as nu
nu.reset_units('SI')

from numericalunits import km, s, day, year, kg, GNewton

import Forces
from VObjects.VBall import VBall

mln_km = 1e6 * km

def clear_trail(vObjects):
    for vObj in vObjects:
        vObj.obj.clear_trail()

def generateSolarSystem(beg=0, end=8):
    offset = vec(20, 20, 0)
    solar_system = [VBall(pos = vec(0,0,0), radius=696340 * 1e1 * km, vel=vec(0, 0, 0), col=color.yellow, mass = 2e30 * kg, label_text="Sun", label_offset = offset),
            VBall(pos = vec(70 * mln_km,0,0), radius= 2440 * 1e3 * km, vel=vec(0, 47 * km / s, 0), col=vec(0.2, 0.2, 0.2), label_text="Mercury", label_offset = offset),
            VBall(pos = vec(110 * mln_km,0,0), radius= 6052 * 1e3 * km, vel=vec(0, 35 * km / s, 0), col=color.orange, label_text="Venus", label_offset = offset),
            VBall(pos = vec(150 * mln_km,0,0), radius= 6378 * 1e3 * km, vel=vec(0, 30 * km / s, 0), col=color.blue, label_text="Earth", label_offset = offset),
            VBall(pos = vec(250 * mln_km,0,0), radius= 3396 * 1e3 * km, vel=vec(0, 24 * km / s, 0), col=color.red, label_text="Mars", label_offset = offset),
            VBall(pos = vec(778 * mln_km,0,0), radius= 71492 * 1e3 * km, vel=vec(0, 13 * km / s, 0), col=color.red, label_text="Jupiter", label_offset = offset),
            VBall(pos = vec(1426 * mln_km,0,0), radius= 60268 * 1e3 * km, vel=vec(0, 9.65 * km / s, 0), col=color.red, label_text="Saturn", label_offset = offset),
            VBall(pos = vec(2870 * mln_km,0,0), radius= 25559 * 1e3 * km, vel=vec(0, 6.81 * km / s, 0), col=color.blue, label_text="Uranus", label_offset = offset),
            VBall(pos = vec(4498 * mln_km,0,0), radius= 24764 * 1e3 * km, vel=vec(0, 5.44 * km / s, 0), col=color.blue, label_text="Neptun", label_offset = offset)]

    return solar_system[beg:end]

def right_top_corner(vObjects):
    max_dist = 0

    for vObj in vObjects:
        if mag(vObj.obj.pos) > max_dist:
            max_dist = mag(vObj.obj.pos)

    return vec(1.5 * max_dist, 1.5 * max_dist, 0)

dt = day / 2
t_end = 28 * year

scene = canvas()
scene.width = 1000
scene.height = 1000

celestial_bodies = generateSolarSystem()
sun = celestial_bodies[0]
planets = celestial_bodies[1:]

reference_point = sun.obj.pos
changed_ref = True

def center_on(ref_pos, vObjects):
    if ref_pos != vec(0, 0, 0):
        pos = copy.copy(ref_pos)
        
        for vObj in vObjects:
            vObj.obj.pos -= pos

    global changed_ref

    if changed_ref:
        clear_trail(vObjects)
        changed_ref = False

def handle_click(ev):
    clicked = scene.mouse.pick
    
    if clicked:
        global reference_point
        global changed_ref
        reference_point = clicked.pos
        changed_ref = True

scene.bind('click', handle_click)

t = 0
tlabel = label(pos = right_top_corner(celestial_bodies), text = str(t))

while t < t_end:
    rate(40)

    t += dt
    tlabel.text = str(round(t / year, 2)) + " Earth years"
    
    for planet in planets:
        planet.apply_force(Forces.computeNewtonGravitation(sun, planet))
        planet.update(dt)

    center_on(reference_point, celestial_bodies)