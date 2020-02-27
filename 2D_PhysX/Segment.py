class Segment(object):
    """The simplest representation of line segment possible"""

    @staticmethod
    def class_id():
        return "Segment"

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.points = (self.point1, self.point2)

    def __del__(self):
        del self.points
        del self.point1
        del self.point2