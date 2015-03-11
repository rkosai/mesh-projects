#!/usr/bin/python

import math
from mesh.generator import Generator
from mesh.shape_primitives import Circle
from mesh.object_model import ObjectModel
from mesh.mesh_utils import MeshUtils
from mesh.shape_utils import ShapeUtils
from objects.joined_pipe import JoinedPipe

PIPE_RADIUS = 1.2
INTER_SIZE = 8
DISTANCE = 10 - 2 * PIPE_RADIUS

##################################################

obj = ObjectModel()

left, right = (None, None)
left_0, right_0 = (None, None)

theta = 0
for i in range(10):
    # Make pipe
    p = JoinedPipe(PIPE_RADIUS)
    p.translate(0, 0, 10 * i)

    obj.add_triangles(p.get_triangles())

    if (right is not None):
        obj.add_triangles(
            ShapeUtils.stitch_shapes(right, p.get_right().get_input()) +
            ShapeUtils.stitch_shapes(left, p.get_left().get_input())
        )
    else:
        right_0 = p.get_right().get_input()
        left_0 = p.get_left().get_input()

    top = 10 * i + PIPE_RADIUS

    right = p.get_right().get_output()
    left = p.get_left().get_output()

    # Make connectors
    for j in range(1, INTER_SIZE):
        z = top + DISTANCE * j / INTER_SIZE
        s1 = Circle(PIPE_RADIUS, True)
        s1.translate(5, 0, z)

        s2 = Circle(PIPE_RADIUS, True)
        s2.translate(-5, 0, z)

        obj.add_triangles(
            ShapeUtils.stitch_shapes(s1, right) +
            ShapeUtils.stitch_shapes(s2, left)
        )

        right = s1
        left = s2

# Build end caps
for end in (right, left, right_0, left_0):
    end.fill_internal_edges()
    obj.add_triangles(end.get_triangles())

# Twist shape
triangles = obj.get_triangles()
obj.set_triangles(MeshUtils.twist_mesh(triangles, ShapeUtils.Z, 100))

# generate a file
generator = Generator()
generator.print_model(obj)

