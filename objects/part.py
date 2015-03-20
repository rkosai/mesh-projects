from mesh.shape_utils import ShapeUtils
class Part:
    def __init__(self):
        self.triangles = []
        self.shapes = []

    def register_external_shape(self, shape):
        self.shapes.append(shape)

    def register_external_parts(self, parts):
        for part in parts:
            self.shapes += part.shapes

    def _apply_to_vectors(self, func, params):
        for i in range(len(self.triangles)):
            new_triangle = []
            for v in self.triangles[i]:
                new_v = func(v, *params)
                new_triangle.append(new_v)
            self.triangles[i] = new_triangle

    def translate(self, dx, dy, dz):
        self._apply_to_vectors(ShapeUtils.translate_v, (dx, dy, dz))
        for shape in self.shapes:
            shape.translate(dx, dy, dz)

    def rotateX(self, theta):
        self._apply_to_vectors(ShapeUtils.rotatev_x, (theta,))
        for shape in self.shapes:
            shape.rotateX(theta)

    def rotateY(self, theta):
        self._apply_to_vectors(ShapeUtils.rotatev_y, (theta,))
        for shape in self.shapes:
            shape.rotateY(theta)

    def rotateZ(self, theta):
        self._apply_to_vectors(ShapeUtils.rotatev_z, (theta,))
        for shape in self.shapes:
            shape.rotateZ(theta)

    def get_mesh(self):
        return self.triangles
