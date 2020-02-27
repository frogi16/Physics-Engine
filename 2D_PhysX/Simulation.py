from vpython import *
import math
import itertools
import random

from SystemQuantities import SystemQuantities

from CollisionsDetection import *
from CollisionsEffects import *
from Collider import Collider

import Utility

class Simulation(object):
    """description of class"""

    def __init__(self, dt, t_end=math.inf, rate=100, scene_size_x=1600, scene_size_y=900):
        self.t = 0
        self.t_end = t_end
        self.dt = dt
        self.rate = rate

        self.scene = canvas()
        self.scene_size(scene_size_x, scene_size_y)

        self.collider = Collider()
        self.system_quantities = SystemQuantities()

        self.tracked_objects = {}

        self.after_update = lambda: None

    def run(self):
        while self.t < self.t_end:
            rate(self.rate)
            self.t += self.dt

            for group in self.tracked_objects.values():
                for object in group:
                    object.update(self.dt)

                self.collider.apply_to_combinations(group, 2)

            for group1, group2 in itertools.combinations(self.tracked_objects.values(), 2):
                self.collider.apply_to_product(group1, group2)

            self.after_update()

    def scene_size(self, width, height):
        self.scene.width = width
        self.scene.height = height

    def track_objects(self, vObjects):
        type = vObjects[0].class_id()

        if type not in self.tracked_objects:
            self.tracked_objects[type] = []
        
        self.tracked_objects[type] += vObjects