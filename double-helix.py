#!/usr/bin/python

import math
from mesh.generator import Generator
from mesh.shape_primitives import Circle
from mesh.object_model import ObjectModel
from mesh.shape_model import ShapeModel
from mesh.mesh_utils import MeshUtils
from objects.tee_pipe import TeePipe
from objects.joined_pipe import JoinedPipe

PIPE_RADIUS = 1.2
INTER_SIZE = 8
SHIFT_ANGLE = math.pi / 10
PIPES_PER_ROTATION = 8

distance = 10 - 2 * PIPE_RADIUS
theta_distance = 2 * math.pi / PIPES_PER_ROTATION

TILT = math.pi / 10

##################################################

obj = ObjectModel()

first_left, first_right = (None, None)
left, right = (None, None)

theta = 0
for i in range(10):
    theta = 2 * math.pi * i / PIPES_PER_ROTATION

    # Make pipe
    p = JoinedPipe(PIPE_RADIUS, TILT)
    p.translate(0, 0, 10 * i)
    p.rotateZ(theta)

    obj.add_triangles(p.get_triangles())

    if (right is not None):
        obj.add_triangles(
            MeshUtils.stitch_shapes(right, p.get_right().get_input(), 'Z') +
            MeshUtils.stitch_shapes(left, p.get_left().get_input(), 'Z')
        )
    else:
        first_right = p.get_right().get_input()
        first_left = p.get_left().get_input()

    top = 10 * i + PIPE_RADIUS

    right = p.get_right().get_output()
    left = p.get_left().get_output()

    # Make connectors
    for j in range(1, INTER_SIZE):
        theta_prime = theta + theta_distance * j / INTER_SIZE
        z = top + distance * j / INTER_SIZE
        s1 = Circle(PIPE_RADIUS, True)
        s1.close_vectors()
        s1.translate(5, 0, z)
        s1.rotateZ(theta_prime)

        s2 = Circle(PIPE_RADIUS, True)
        s2.close_vectors()
        s2.translate(-5, 0, z)
        s2.rotateZ(theta_prime)

        obj.add_triangles(
            MeshUtils.stitch_shapes(right, s1, 'Z') +
            MeshUtils.stitch_shapes(left, s2, 'Z')
        )

        right = s1
        left = s2

right.fill_internal_edges()
left.fill_internal_edges()

first_right.fill_internal_edges()
first_left.fill_internal_edges()

obj.add_triangles(
    right.get_triangles() + left.get_triangles() +
    first_right.get_triangles() + first_left.get_triangles()
)

# generate a file
generator = Generator()
generator.print_model(obj)

