from random import uniform
from vpython import vec

def randomVec(min, max):
    """Value of each component of vector will be randomized within specified range. Magnitude of resultant vector is unspecified."""
    return vec(uniform(min, max), uniform(min, max), uniform(min, max))

def randomColor():
    """Random color represented as VPython's vec."""
    return randomVec(0, 1)

def perp_product(A, B):
    """2D equivalent of dot product. |A|*|B|*sin( <)(A, B) )"""
    return A.x * B.y - A.y * B.x