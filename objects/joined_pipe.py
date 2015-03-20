import math
from part import Part
from tee_pipe import TeePipe
from mesh.shape_utils import ShapeUtils

class JoinedPipe(Part):
    def __init__(self, radius):
        Part.__init__(self)

        # Right side
        p1 = TeePipe(radius)
        p1.rotateZ(math.pi)
        p1.translate(5, 0, 0)

        # Left side
        p2 = TeePipe(radius)
        p2.translate(-5, 0, 0)

        # Register external shapes
        self.register_external_parts([p1, p2])

        # Join pipes
        t1 = p1.tap
        t2 = p2.tap

        # Set up triangles
        self.triangles = p1.get_mesh() + p2.get_mesh() + \
                         ShapeUtils.stitch_shapes(t2, t1)

        self.right = p1
        self.left = p2
