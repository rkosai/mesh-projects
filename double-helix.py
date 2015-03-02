#!/usr/bin/python

import math
from mesh.generator import Generator
from mesh.shape_primitives import Circle
from mesh.object_model import ObjectModel
from mesh.shape_model import ShapeModel
from mesh.mesh_utils import MeshUtils
from objects.tee_pipe import TeePipe

PIPE_RADIUS = 1.2

##################################################

def make_pipe():
    p1 = TeePipe(PIPE_RADIUS)
    p1.rotateZ(math.pi)
    p1.translate(5, 0, 0)

    p2 = TeePipe(PIPE_RADIUS)
    p2.translate(-5, 0, 0)

    return p1, p2

def stitch_taps(p1, p2):
    t1 = p1.get_tap()
    t2 = p2.get_tap()
    t1.reverse_edges()
    return MeshUtils.stitch_shapes(t1, t2)

obj = ObjectModel()

first_left, first_right = (None, None)
left, right = (None, None)

theta = 0
for i in range(5):
    theta = 2 * math.pi * i / 5
    theta_distance = 2 * math.pi / 5

    # Make pipe
    p1, p2 = make_pipe()
    p1.translate(0, 0, 10 * i)
    p2.translate(0, 0, 10 * i)

    p1.rotateZ(theta)
    p2.rotateZ(theta)

    bar_triangles = stitch_taps(p1, p2)

    obj.add_triangles(
        p1.get_triangles() +
        p2.get_triangles() +
        bar_triangles
    )

    if (right is not None):
        obj.add_triangles(
            MeshUtils.stitch_shapes(right, p1.get_input()) +
            MeshUtils.stitch_shapes(left, p2.get_input())
        )

    top = 10 * i + PIPE_RADIUS
    bottom = 10 * i - PIPE_RADIUS
    distance = 10 - 2 * PIPE_RADIUS

    right = p1.get_output()
    left = p2.get_output()

    # Make connectors
    for j in range(1, 4):
        theta_prime = theta + theta_distance * j / 4
        z = top + distance * j / 4
        s1 = Circle(PIPE_RADIUS, True)
        s1.close_vectors()
        s1.translate(5, 0, z)
        s1.rotateZ(theta_prime)

        s2 = Circle(PIPE_RADIUS, True)
        s2.close_vectors()
        s2.translate(-5, 0, z)
        s2.rotateZ(theta_prime)

        obj.add_triangles(
            MeshUtils.stitch_shapes(right, s1) +
            MeshUtils.stitch_shapes(left, s2)
        )

        right = s1
        left = s2

# generate a file
generator = Generator()
generator.print_model(obj)

