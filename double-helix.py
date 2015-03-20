#!/usr/bin/python

from mesh.generator import Generator
from mesh.mesh_utils import MeshUtils
from mesh.object_model import ObjectModel
from objects.joined_pipe import JoinedPipe
from objects.segmented_pipe import SegmentedPipe

PIPE_RADIUS = 1.2
DISTANCE = 10 - 2 * PIPE_RADIUS

##################################################

obj = ObjectModel()
left_0, right_0 = (None, None)

for z in range(0, 100, 10):
    p = JoinedPipe(PIPE_RADIUS)
    p.translate(0, 0, z)

    if right_0 is None:
        right_0, left_0 = (p.right.input, p.left.input)

    s1 = SegmentedPipe(PIPE_RADIUS, DISTANCE, 8)
    s2 = SegmentedPipe(PIPE_RADIUS, DISTANCE, 8)

    s1.translate(5, 0, z + PIPE_RADIUS)
    s2.translate(-5, 0, z + PIPE_RADIUS)

    for part in [p, s1, s2]:
        obj.add_mesh(part.get_mesh())

# Build end caps
for end in (s1.top, s2.top, right_0, left_0):
    end.fill_internal_edges()
    obj.add_mesh(end.get_triangles())

# Twist shape
obj.apply_transform(MeshUtils.twist_mesh, (MeshUtils.Z, 100))

# generate a file
generator = Generator()
generator.print_model(obj)
