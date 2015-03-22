#!/usr/bin/python

import math
from mesh.generator import Generator
from mesh.mesh_utils import MeshUtils
from mesh.object_model import ObjectModel
from objects.joined_pipe import JoinedPipe
from objects.segmented_pipe import SegmentedPipe

PIPE_RADIUS = 0.7
LENGTH = 7  # Between pipes
HALF_WIDTH = 3.75  # Betwen strands
BRACELET_RADIUS = 75 / float(2)
REVOLUTIONS = 2
GAIN = 15  # Millimeters per revolution

SEGMENT_LENGTH = LENGTH - 2 * PIPE_RADIUS
LENGTH_UNITS = 2 * math.pi * BRACELET_RADIUS / LENGTH

##################################################

obj = ObjectModel()
left_0, right_0 = (None, None)

for z in range(0, int(LENGTH_UNITS * REVOLUTIONS) * LENGTH, LENGTH):
    p = JoinedPipe(PIPE_RADIUS, HALF_WIDTH)
    p.translate(0, 0, z)

    if right_0 is None:
        right_0, left_0 = (p.right.input, p.left.input)

    s1 = SegmentedPipe(PIPE_RADIUS, SEGMENT_LENGTH, 8)
    s2 = SegmentedPipe(PIPE_RADIUS, SEGMENT_LENGTH, 8)

    s1.translate(HALF_WIDTH, 0, z + PIPE_RADIUS)
    s2.translate(-1 * HALF_WIDTH, 0, z + PIPE_RADIUS)

    for part in [p, s1, s2]:
        obj.add_mesh(part.get_mesh())

# Build end caps
for end in (s1.top, s2.top, right_0, left_0):
    end.fill_internal_edges()
    obj.add_mesh(end.get_triangles())

# Twist shape
obj.apply_transform(MeshUtils.twist_mesh, (MeshUtils.Z, LENGTH * 10))
obj.apply_transform(MeshUtils.translate, (0, 0, BRACELET_RADIUS))
obj.apply_transform(MeshUtils.spiral, (MeshUtils.Y, LENGTH_UNITS, GAIN))

# generate a file
generator = Generator()
generator.print_model(obj)