from vpython import *
import math
import itertools
import random
import numpy as np

from VBall import VBall

def generateVBallsClassic(ballsCount, left_top_corner, right_down_corner, min_vel, max_vel, radius, mass):
    balls = []

    while len(balls) < ballsCount:
        position = vec(random.uniform(left_top_corner.x, right_down_corner.x), random.uniform(right_down_corner.y, left_top_corner.y), 0)
        velocity = vec(random.uniform(min_vel, max_vel), random.uniform(min_vel, max_vel), 0)

        is_colliding = False
        for ball in balls:
            if mag(ball.obj.pos - position) < 2 * radius:
                is_colliding = True
                break

        if not is_colliding:
            balls.append(VBall(pos = position, radius = radius, mass = mass, vel = velocity, col = randomColor(), make_trail = False))

    return balls

def generateVBalls(ballsCount, left_top_corner, right_down_corner, min_vel, max_vel, radius, mass):
    balls = []

    while len(balls) < ballsCount:
        positions = np.column_stack((np.random.uniform(left_top_corner.x, right_down_corner.x, ballsCount),
                                  np.random.uniform(right_down_corner.y, left_top_corner.y, ballsCount),
                                  np.zeros(ballsCount)))
        velocities = np.column_stack((np.random.uniform(min_vel, max_vel, ballsCount),
                                  np.random.uniform(min_vel, max_vel, ballsCount),
                                  np.zeros(ballsCount)))

        list_to_vec = lambda list: vec(*list)
        positions = np.apply_along_axis(list_to_vec, 1, positions)
        velocities = np.apply_along_axis(list_to_vec, 1, velocities)

        distances = np.ndarray((ballsCount, ballsCount), dtype = 'O')
        
        for i in range(ballsCount):
            distances[i:-1, i] = positions[i:-1] - positions[i]

        for i in range(len(distances) - 1,-1, -1):
            to_remove = False

            for dist_vec in distances[i,:]:
                test = (dist_vec is not None) and (mag(dist_vec) < 2)
                if test:
                    to_remove = True
                    break

            if to_remove:
                positions = np.delete(positions, i)

        batch_of_balls = [VBall(pos = positions[i], radius = radius, mass = mass, vel = velocities[i], col = randomColor(), make_trail = False) for i in range(len(positions))]

        colliding_balls_indices = [i for ball1 in balls + batch_of_balls for i, ball2 in enumerate(batch_of_balls) if collisionDetectedBalls(ball1, ball2)]
        colliding_balls_indices = list(set(colliding_balls_indices))   #remove duplicates
        colliding_balls_indices.sort(reverse = True)

        for i in colliding_balls_indices:
            batch_of_balls[i].destroy()
            del batch_of_balls[i]

        while len(balls) + len(batch_of_balls) > ballsCount:
            batch_of_balls.pop(-1).destroy()

        balls = balls + batch_of_balls

    colliding_count = len([i for ball1 in balls for i, ball2 in enumerate(balls) if collisionDetectedBalls(ball1, ball2)])

    return balls

import timeit

def testGeneratingClassic():
    balls = generateVBallsClassic(50, vec(-10, 10, 0), vec(10, -10, 0), -5, 5, 1, 1)

    for ball in balls:
        ball.destroy()
        del ball

    balls = []

def testGenerating():
    balls = generateVBallsClassic(50, vec(-10, 10, 0), vec(10, -10, 0), -5, 5, 1, 1)

    for ball in balls:
        ball.destroy()
        del ball

    balls = []

timeClassic = timeit.timeit(testGeneratingClassic, number=1000)
print(timeClassic)		#19.3536623

time = timeit.timeit(testGenerating, number=1000)
print(time)				#16.5252897