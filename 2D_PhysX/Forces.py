from vpython import vec
from vpython import mag
from vpython import norm

from numericalunits import GNewton

def computeQuadraticAirResistance(object, drag_coefficient):
    return - drag_coefficient * mag(object.vel) ** 2 * norm(object.vel)

def computeLinearAirResistance(object, drag_coefficient):
    return - drag_coefficient * object.vel

def computeNewtonGravitation(source, object, gravitational_constant=GNewton):
    r = object.obj.pos - source.obj.pos
    return r * -gravitational_constant * source.mass / (mag(r) ** 3)