#!/usr/bin/python

from mesh.generator import Generator
from mesh.mesh_utils import MeshUtils
from mesh.object_model import ObjectModel
from mesh.shape_utils import ShapeUtils
from objects.joined_pipe import JoinedPipe
from objects.segmented_pipe import SegmentedPipe

PIPE_RADIUS = 1.2
INTER_SIZE = 8
DISTANCE = 10 - 2 * PIPE_RADIUS

##################################################

obj = ObjectModel()
left_0, right_0 = (None, None)

for i in range(10):
    z = 10 * i

    # Make pipe
    p = JoinedPipe(PIPE_RADIUS)
    p.translate(0, 0, z)
    obj.add_mesh(p.get_triangles())

    if right_0 is None:
        right_0, left_0 = (p.right.input, p.left.input)

    s1 = SegmentedPipe(PIPE_RADIUS, DISTANCE, 8)
    s2 = SegmentedPipe(PIPE_RADIUS, DISTANCE, 8)
    s1.translate(5, 0, z + PIPE_RADIUS)
    s2.translate(-5, 0, z + PIPE_RADIUS)

    obj.add_mesh(s1.get_triangles() + s2.get_triangles())

# Build end caps
for end in (s1.top, s2.top, right_0, left_0):
    end.fill_internal_edges()
    obj.add_mesh(end.get_triangles())

# Twist shape
triangles = obj.get_mesh()
obj.set_mesh(MeshUtils.twist_mesh(triangles, ShapeUtils.Z, 100))

# generate a file
generator = Generator()
generator.print_model(obj)
