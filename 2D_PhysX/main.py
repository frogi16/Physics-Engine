from vpython import *
import math
import itertools
import copy
import matplotlib.pyplot as plt
import random

class SystemMomentum:
    def __init__(self):
        self.systemMomentum = vec(0, 0, 0)
        self.systemMomentumAbs = 0
        self.arrow = arrow(pos = vec(20, 20, 0), axis = self.systemMomentum, scale=2, shaftwidth=0.2)

    def computeBalls(self, balls):
        systemMomentumTemp = vec(0, 0, 0)
        systemMomentumTempAbs = 0

        for ball in balls:
            systemMomentumTemp += momentumOfVball(ball)
            systemMomentumTempAbs += mag(momentumOfVball(ball))

        diff = abs(self.systemMomentumAbs - systemMomentumTempAbs)
        if self.systemMomentumAbs != 0 and diff > 0.1:
            test = True

        self.systemMomentumAbs = copy.copy(systemMomentumTempAbs)
        self.systemMomentum = copy.copy(systemMomentumTemp)
        self.arrow.axis = systemMomentumTemp

class CircularBuffer:
    def __init__(self, buffer_size=1):
        self.buffer_size = buffer_size
        self.list = buffer_size * [None]
        self.index = 0

    def val(self):
        return copy.copy(self.list[self.index])

    def push(self, value):
        self.index = (self.index + 1) % self.buffer_size
        self.list[self.index] = copy.copy(value)

    def pop(self):
        self.list[self.index] = None
        self.index = (self.index - 1) % self.buffer_size

class Vball:
    def __init__(self, pos, radius=1, mass=1, vel=vec(0, 0, 0), col=color.white, make_trail=True):
        self.mass = mass
        self.ball = sphere(pos = pos, radius = radius, vel = vel, color=col, make_trail = make_trail)
        self.arrow = attach_arrow(self.ball, "vel", scale=2, shaftwidth=0.2)
        self.circular_buffer = CircularBuffer()

    def __delete__(self):
        del self.mass
        del self.ball
        del self.arrow
        del self.circular_buffer

    def update(self, dt):
        self.circular_buffer.push(self.ball.pos)
        self.ball.pos += self.ball.vel * dt
        
    def reverseUpdate(self):
        previousPos = self.circular_buffer.val()

        if previousPos != None:
            self.ball.pos = previousPos

        self.circular_buffer.pop()
        return previousPos
        

class Vwall:
    def __init__(self, pos, size=vec(1, 1, 1), color=color.white):
        self.wall = box(pos = pos, size = size, color = color)

def energyOfVball(vball):
    return 0.5 * vball.mass * mag(vball.ball.vel) ** 2

def momentumOfVball(vball):
    return vball.mass * vball.ball.vel

def collisionDetected(vball, vwall):
    bpos = vball.ball.pos
    wpos = vwall.wall.pos
    wsize = vwall.wall.size

    collisionLeft = collisionDetectedCircleSegment(vball, vec(wpos.x - wsize.x, wpos.y - wsize.y, 0), vec(wpos.x - wsize.x, wpos.y + wsize.y, 0))
    collisionRight = collisionDetectedCircleSegment(vball, vec(wpos.x + wsize.x, wpos.y - wsize.y, 0), vec(wpos.x + wsize.x, wpos.y + wsize.y, 0))
    collisionTop = collisionDetectedCircleSegment(vball, vec(wpos.x - wsize.x, wpos.y + wsize.y, 0), vec(wpos.x + wsize.x, wpos.y + wsize.y, 0))
    collisionDown = collisionDetectedCircleSegment(vball, vec(wpos.x - wsize.x, wpos.y - wsize.y, 0), vec(wpos.x + wsize.x, wpos.y - wsize.y, 0))
    
    if collisionLeft or collisionRight:
        return True, "x"
    elif collisionTop or collisionDown:
        return True, "y"
    else:
        return False

def collisionDetectedCircleSegment(vball, point1, point2):
    if point1 != point2:
        centerProjectedOnSegment = proj(vball.ball.pos - point1, point2 - point1) + point1
        return mag(vball.ball.pos - centerProjectedOnSegment) <= vball.ball.radius
    return None

def collisionDetectedBalls(ball1, ball2):
    if ball1 == ball2:
        return False
    
    pos1 = ball1.ball.pos
    pos2 = ball2.ball.pos

    rad1 = ball1.ball.radius
    rad2 = ball2.ball.radius

    return mag(pos2 - pos1) <= rad1 + rad2

def applyCollision(ball1, ball2):
    vel1 = mag(ball1.ball.vel)
    vel2 = mag(ball2.ball.vel)
    
    theta1 = math.atan2(ball1.ball.vel.y, ball1.ball.vel.x)
    theta2 = math.atan2(ball2.ball.vel.y, ball2.ball.vel.x)
    dPos = ball1.ball.pos - ball2.ball.pos
    phi = math.atan2(dPos.y, dPos.x)

    v1partial_factor = (vel1 * cos(theta1 - phi) * (ball1.mass - ball2.mass) + 2 * ball2.mass * vel2 * cos(theta2 - phi)) / (ball1.mass + ball2.mass)
    v2partial_factor = (vel2 * cos(theta2 - phi) * (ball2.mass - ball1.mass) + 2 * ball1.mass * vel1 * cos(theta1 - phi)) / (ball1.mass + ball2.mass)

    ball1.ball.vel.x = v1partial_factor * cos(phi) + vel1 * sin(theta1 - phi) * cos(phi + math.pi / 2)
    ball2.ball.vel.x = v2partial_factor * cos(phi) + vel2 * sin(theta2 - phi) * cos(phi + math.pi / 2)

    ball1.ball.vel.y = v1partial_factor * sin(phi) + vel1 * sin(theta1 - phi) * sin(phi + math.pi / 2)
    ball2.ball.vel.y = v2partial_factor * sin(phi) + vel2 * sin(theta2 - phi) * sin(phi + math.pi / 2)

    ball1.reverseUpdate()
    ball2.reverseUpdate()

def applyCollisionRewrite(ball1, ball2):
    dPos = ball1.ball.pos - ball2.ball.pos
    collision_angle = math.atan2(dPos.y,dPos.x)

    vel1 = mag(ball1.ball.vel)
    vel2 = mag(ball2.ball.vel)

    direction_1 = math.atan2(ball1.ball.vel.y, ball1.ball.vel.x)
    direction_2 = math.atan2(ball2.ball.vel.y, ball2.ball.vel.x)

    new_xspeed_1 = vel1 * math.cos(direction_1 - collision_angle)
    new_xspeed_2 = vel2 * math.cos(direction_2 - collision_angle)
    
    final_xspeed_1 = ((ball1.mass - ball2.mass) * new_xspeed_1 + (ball2.mass + ball2.mass) * new_xspeed_2) / (ball1.mass + ball2.mass)
    final_xspeed_2 = ((ball1.mass + ball1.mass) * new_xspeed_1 + (ball2.mass - ball1.mass) * new_xspeed_2) / (ball1.mass + ball2.mass)
    
    final_yspeed_1 = vel1 * math.sin(direction_1 - collision_angle)
    final_yspeed_2 = vel2 * math.sin(direction_2 - collision_angle)

    ball1.ball.vel.x = math.cos(collision_angle) * final_xspeed_1 + math.cos(collision_angle + math.pi / 2) * final_yspeed_1
    ball1.ball.vel.y = math.sin(collision_angle) * final_xspeed_1 + math.sin(collision_angle + math.pi / 2) * final_yspeed_1
    ball2.ball.vel.x = math.cos(collision_angle) * final_xspeed_2 + math.cos(collision_angle + math.pi / 2) * final_yspeed_2
    ball2.ball.vel.y = math.sin(collision_angle) * final_xspeed_2 + math.sin(collision_angle + math.pi / 2) * final_yspeed_2

    ball1.reverseUpdate()
    ball2.reverseUpdate()

scene = canvas()
scene.width = 1000
scene.height = 1000
scene.range = 2
scene.autoscale = True

#balls = [Vball(pos = vec(2, 6, 0), vel = vec(2, 2, 0), radius = 1, mass = 1,
#col = color.red, make_trail = True),
#         Vball(pos = vec(7, 8, 0), vel = vec(-0.8, -1.3, 0), radius = 1.7,
#         mass = 4, col = color.green, make_trail = True),
#         Vball(pos = vec(2, -6, 0), vel = vec(-0.9, 0.9, 0), radius = 1, mass
#         = 1, col = color.purple, make_trail = True),
#         Vball(pos = vec(-5, 5, 0), vel = vec(1.3, -1, 0), radius = 1.5, mass
#         = 3, col = color.cyan, make_trail = True),
#         Vball(pos = vec(-7, 1, 0), vel = vec(0.3, -2.4, 0), radius = 1.3,
#         mass = 2, col = color.blue, make_trail = True),
#         Vball(pos = vec(-7, -8, 0), vel = vec(-1.2, 1.4, 0), radius = 1, mass
#         = 1, col = color.orange, make_trail = True)]
balls = [Vball(pos = vec(random.uniform(-10, 10), random.uniform(-10, 10), 0), vel = vec(random.uniform(-4, 4), random.uniform(-4, 4), 0), col = vec(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)), make_trail = True) for i in range(20)]

test = [i for ball1 in balls for i, ball2 in enumerate(balls) if collisionDetectedBalls(ball1, ball2)]
test.sort(reverse = True)
test = list(set(test))

for i in test[::-1]:
    balls[i].ball.visible = False
    balls[i].arrow.visible = False
    del balls[i]

to_remove = len(balls) * [False]
for ball in balls:
    for i, ball2 in enumerate(balls):
        if collisionDetectedBalls(ball, ball2):
            to_remove[i] = True

walls = [Vwall(vec(-12, 0, 0), vec(2, 30, 2), color.magenta),
         Vwall(vec(12, 0, 0), vec(2, 30, 2), color.magenta),
         Vwall(vec(0, -12, 0), vec(30, 2, 2), color.magenta),
         Vwall(vec(0, 12, 0), vec(30, 2, 2), color.magenta)]

dt = 0.005
t = 0
energies = []
momentums = []
system_momentum = SystemMomentum()

while t < 50:
    rate(120)

    t += dt
    
    system_momentum.computeBalls(balls)
    momentums.append(system_momentum.systemMomentumAbs)

    systemEnergy = 0

    for ball in balls:
        systemEnergy += energyOfVball(ball)
        ball.update(dt)

    energies.append(systemEnergy)

    for pair in itertools.product(balls, walls):
        vball = pair[0]
        vwall = pair[1]

        bpos = vball.ball.pos
        wpos = vwall.wall.pos
        wsize = vwall.wall.size

        collisionLeft = collisionDetectedCircleSegment(vball, vec(wpos.x - wsize.x / 2, wpos.y - wsize.y / 2, 0), vec(wpos.x - wsize.x / 2, wpos.y + wsize.y / 2, 0))
        collisionRight = collisionDetectedCircleSegment(vball, vec(wpos.x + wsize.x / 2, wpos.y - wsize.y / 2, 0), vec(wpos.x + wsize.x / 2, wpos.y + wsize.y / 2, 0))
        collisionTop = collisionDetectedCircleSegment(vball, vec(wpos.x - wsize.x / 2, wpos.y + wsize.y / 2, 0), vec(wpos.x + wsize.x / 2, wpos.y + wsize.y / 2, 0))
        collisionDown = collisionDetectedCircleSegment(vball, vec(wpos.x - wsize.x / 2, wpos.y - wsize.y / 2, 0), vec(wpos.x + wsize.x / 2, wpos.y - wsize.y / 2, 0))

        if collisionLeft or collisionRight:
            vball.ball.vel.x *= -1
        elif collisionTop or collisionDown:
            vball.ball.vel.y *= -1

    for pair in itertools.combinations(balls, 2):
        if collisionDetectedBalls(*pair):
            energyBefore = energyOfVball(pair[0]) + energyOfVball(pair[1])
            momentumBefore = momentumOfVball(pair[0]) + momentumOfVball(pair[1])
            #applyCollision(*pair)
            applyCollisionRewrite(*pair)
            energyAfter = energyOfVball(pair[0]) + energyOfVball(pair[1])
            momentumAfter = momentumOfVball(pair[0]) + momentumOfVball(pair[1])

            if energyAfter - energyBefore > 0.01 or mag(momentumAfter - momentumBefore) > 0.01:
                test = True

plt.plot(range(1, len(energies) + 1), energies)
plt.plot(range(1, len(momentums) + 1), momentums)
plt.xlabel("time [ticks]")
plt.ylabel("system energy [J]")
plt.show()