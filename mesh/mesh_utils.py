import math
from shape_utils import ShapeUtils

class MeshUtils:

    @staticmethod
    def twist_mesh(triangles, axis, dpt):
        new_triangles = []
        func = ShapeUtils.get_rotatev_func(axis)

        for triangle in triangles:
            new_t = []
            for v in triangle:
                if axis == ShapeUtils.X:
                    index = v[0]
                elif axis == ShapeUtils.Y:
                    index = v[1]
                elif axis == ShapeUtils.Z:
                    index = v[2]

                rotation = (index % dpt) / float(dpt) * 2 * math.pi
                new_v = func(v, rotation)
                new_t.append(new_v)
            new_triangles.append(new_t)

        return new_triangles

