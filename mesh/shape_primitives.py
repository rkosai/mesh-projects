from shape_model import ShapeModel
import math

class Polygon(ShapeModel):
    def __init__(self, r, points, up):
        ShapeModel.__init__(self)

        point_list = range(points)
        if not up:
            point_list.reverse()

        for i in point_list:
            theta = 2 * math.pi * i / points
            self.add_vector(r * math.cos(theta), r * math.sin(theta), 0)

class Circle(Polygon):
    def __init__(self, r, up):
        Polygon.__init__(self, r, 50, up)


