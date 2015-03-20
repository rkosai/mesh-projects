#!/usr/bin/python

from mesh.generator import Generator
from mesh.shape_primitives import Circle
from mesh.object_model import ObjectModel
from mesh.mesh_utils import MeshUtils
from mesh.shape_utils import ShapeUtils
from objects.joined_pipe import JoinedPipe

PIPE_RADIUS = 1.2
DISTANCE = 10 - 2 * PIPE_RADIUS

##################################################

obj = ObjectModel()

left_0, right_0 = (None, None)

theta = 0
for i in range(10):
    top = 10 * i + PIPE_RADIUS

    # Make pipe
    p = JoinedPipe(PIPE_RADIUS)
    p.translate(0, 0, 10 * i)

    if right_0 is None:
        right_0 = p.right.input
        left_0 = p.left.input

    # Make connectors
    s1 = Circle(PIPE_RADIUS, True)
    s1.translate(5, 0, top + DISTANCE)

    s2 = Circle(PIPE_RADIUS, True)
    s2.translate(-5, 0, top + DISTANCE)

    conn_mesh = ShapeUtils.stitch_shapes(s1, p.right.output)
    conn_mesh += ShapeUtils.stitch_shapes(s2, p.right.output)

    # Increase resolution of connectors
    conn_mesh = MeshUtils.subdivide_mesh(conn_mesh, 2)
    obj.add_triangles(p.get_triangles() + conn_mesh)

# Build end caps
for end in (s1, s2, right_0, left_0):
    end.fill_internal_edges()
    obj.add_triangles(end.get_triangles())

# Twist shape
obj.set_triangles(MeshUtils.twist_mesh(obj.get_triangles(), ShapeUtils.Z, 100))

# generate a file
generator = Generator()
generator.print_model(obj)
