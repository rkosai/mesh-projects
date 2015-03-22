from part import Part
from mesh.shape_primitives import Circle
from mesh.shape_utils import ShapeUtils

class SegmentedPipe(Part):
    def __init__(self, radius, length, segments):
        Part.__init__(self)

        self.bottom = Circle(radius, False)
        current = self.bottom

        for i in range(1, segments + 1):
            z = length * i / float(segments)

            self.top = Circle(radius, True)
            self.top.translate(0, 0, z)
            self.register_external_shape(self.top)

            self.triangles += ShapeUtils.stitch_shapes(self.top, current)

            current = self.top
