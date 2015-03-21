import math
from shape_utils import ShapeUtils

class MeshUtils:
    X = 'X'
    Y = 'Y'
    Z = 'Z'

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

    @staticmethod
    def _apply_vector_function(triangles, vfunc, params):
        output = []
        for t in triangles:
            output.append([ vfunc(v, *params)for v in t ])
        return output

    @staticmethod
    def translate(triangles, dx, dy, dz):
        return MeshUtils._apply_vector_function(
            triangles, ShapeUtils.translate_v, (dx, dy, dz)
        )

    @staticmethod
    def rotate_x(triangles, theta):
        # TBD
        return triangles

    @staticmethod
    def spiral(triangles, axis, height_per_revolution, gain):
        # TBD
        return triangles

    @staticmethod
    def _find_midpoint(p1, p2):
        x = (p1[0] + p2[0]) / float(2)
        y = (p1[1] + p2[1]) / float(2)
        z = (p1[2] + p2[2]) / float(2)
        return (x, y, z)

    @staticmethod
    def subdivide_mesh(triangles, iterations=1):
        iterations -= 1

        output = []
        for t in triangles:
            i1, i2, i3 = t[0], t[1], t[2]
            j1 = MeshUtils._find_midpoint(i1, i2)
            j2 = MeshUtils._find_midpoint(i2, i3)
            j3 = MeshUtils._find_midpoint(i1, i3)

            output.append([i1, j1, j3])
            output.append([j1, i2, j2])
            output.append([j3, j2, i3])
            output.append([j1, j2, j3])

        if iterations <= 0:
            return output
        else:
            return MeshUtils.subdivide_mesh(output, iterations)

