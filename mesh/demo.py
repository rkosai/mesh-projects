from object_model import ObjectModel
from shape_utils import ShapeUtils
from shape_model import ShapeModel
from shape_primitives import Polygon, Circle

class DemoFactory:

    def _construct3d(self, func):
        s1 = func(-1, False)
        s2 = func(1, True)

        obj = ObjectModel()
        obj.add_triangles(s1.get_triangles())
        obj.add_triangles(s2.get_triangles())
        obj.add_triangles(ShapeUtils.stitch_shapes(s1, s2))

        return obj

    def make_cube(self):
        def make_square(z, up):
            sm = Polygon(1, 4, up)
            sm.fill_internal_edges()
            sm.translate(0, 0, z)
            return sm

        return self._construct3d(make_square)

    def make_oct_prism(self):
        def make_oct(z, up):
            sm = Polygon(1, 8, up)
            sm.fill_internal_edges()
            sm.translate(0, 0, z)
            return sm

        return self._construct3d(make_oct)

    def make_cylinder(self):
        def make_circle(z, up):
            sm = Circle(1, up)
            sm.fill_internal_edges()
            sm.translate(0, 0, z)
            return sm

        return self._construct3d(make_circle)

