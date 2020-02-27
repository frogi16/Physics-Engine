from vpython import vec

from vpython import mag
from vpython import proj

from VObjects.VBall import VBall
from VObjects.VWall import VWall

def colliding_circle_segment(vBall, segment):
    (point1, point2) = segment.points

    if point1 == point2:
        return False
    else:
        centerProjectedOnSegment = proj(vBall.obj.pos - point1, point2 - point1) + point1
        return mag(vBall.obj.pos - centerProjectedOnSegment) <= vBall.obj.radius

def colliding_ball_wall(vBall, vWall):
    collisionLeft = colliding_circle_segment(vBall, vWall.segment_left)
    collisionRight = colliding_circle_segment(vBall, vWall.segment_right)
    collisionTop = colliding_circle_segment(vBall, vWall.segment_top)
    collisionDown = colliding_circle_segment(vBall, vWall.segment_down)
    
    if collisionLeft or collisionRight:
        return "x"
    if collisionTop or collisionDown:
        return "y"
    else:
        False

def colliding_balls(ball1, ball2):
    if ball1 == ball2:
        return False
    
    pos1 = ball1.obj.pos
    pos2 = ball2.obj.pos

    rad1 = ball1.obj.radius
    rad2 = ball2.obj.radius

    return mag(pos2 - pos1) <= rad1 + rad2

def colliding_boxes(box1, box2):
    """Determine if there is a collision between box-shaped objects.

    Keyword arguments:
    box1 -- VObject or its subclass, has to have .obj.pos and .obj.size.(x/y)
    box2 -- exactly as above
    """

    if box1 == box2:
        return False

    left1 = box1.obj.pos.x - box1.obj.size.x / 2
    right1 = box1.obj.pos.x + box1.obj.size.x / 2
    top1 = box1.obj.pos.y + box1.obj.size.y / 2
    down1 = box1.obj.pos.y - box1.obj.size.y / 2

    left2 = box2.obj.pos.x - box2.obj.size.x / 2
    right2 = box2.obj.pos.x + box2.obj.size.x / 2
    top2 = box2.obj.pos.y + box2.obj.size.y / 2
    down2 = box2.obj.pos.y - box2.obj.size.y / 2
    
    return (left1 < right2 and right1 > left2 and down1 < top2 and top1 > down2)