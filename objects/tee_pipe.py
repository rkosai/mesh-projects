import math
from mesh.shape_model import ShapeModel
from mesh.shape_utils import ShapeUtils
from mesh.shape_primitives import Circle
from part import Part

class TeePipe(Part):
    POINTS = 50

    def __init__(self, radius):
        Part.__init__(self)

        # basic pipes
        self.input = Circle(radius, False)
        self.input.close_vectors()
        self.input.translate(0, 0, -1 * radius)
        self.register_external_shape(self.input)

        self.output = Circle(radius, True)
        self.output.close_vectors()
        self.output.translate(0, 0, radius)
        self.register_external_shape(self.output)

        self.tap = Circle(radius, True)
        self.tap.close_vectors()
        self.tap.rotateY(3 * math.pi / 2)
        self.tap.translate(radius, 0, 0)
        self.register_external_shape(self.tap)

        # intersection lines
        int_1 = ShapeModel()
        int_2 = ShapeModel()

        half_vectors_1 = []
        half_vectors_2 = []
        inner_point = None

        for i in range(TeePipe.POINTS):
            theta = 2 * math.pi * i / TeePipe.POINTS
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)

            if (theta >= math.pi / 2) and (theta <= 3 * math.pi / 2):
                z = 0
                if inner_point is None:
                    inner_point = [x, y, z]

            else:
                z = radius * math.cos(theta)

            if (z > 0) and (theta < math.pi):
                half_vectors_1.append([x, y, z])
            elif (z > 0) and (theta > math.pi):
                half_vectors_2.append([x, y, z])

            int_1.add_vector(x, y, -1 * z)
            int_2.add_vector(x, y, z)

        int_1.close_vectors()
        int_2.close_vectors()

        # generate intermediate intersection shape
        int_3 = ShapeModel()
        for v in half_vectors_1:
            int_3.add_vector(*v)

        int_3.add_vector(*inner_point)

        for v in reversed(half_vectors_1):
            int_3.add_vector(v[0], v[1], -1 * v[2])

        for v in reversed(half_vectors_2):
            int_3.add_vector(v[0], v[1], -1 * v[2])

        int_3.add_vector(inner_point[0], -1 * inner_point[1], inner_point[2])

        for v in half_vectors_2:
            int_3.add_vector(*v)

        int_3.close_vectors()

        self.triangles += ShapeUtils.stitch_shapes(int_1, self.input)
        self.triangles += ShapeUtils.stitch_shapes(self.output, int_2)
        self.triangles += ShapeUtils.stitch_shapes(int_3, self.tap)

    def get_input(self):
        return self.input

    def get_output(self):
        return self.output

    def get_tap(self):
        return self.tap
