#!/usr/bin/python

import math
from mesh.generator import Generator
from mesh.shape_primitives import Circle
from mesh.object_model import ObjectModel
from mesh.shape_model import ShapeModel
from mesh.mesh_utils import MeshUtils
from objects.tee_pipe import TeePipe

##################################################

def make_pipe():
    p1 = TeePipe(1)
    p1.rotateY(math.pi)
    p1.translate(5, 0, 0)

    p2 = TeePipe(1)
    p2.translate(-5, 0, 0)

    # join taps
    t1 = p1.get_tap()
    t2 = p2.get_tap()
    t1.reverse_edges()
    triangles = MeshUtils.stitch_shapes(t1, t2)

    return p1, p2, triangles

pipe1, pipe2, triangles = make_pipe()

obj = ObjectModel()
obj.add_triangles(pipe1.get_triangles())
obj.add_triangles(pipe2.get_triangles())
obj.add_triangles(triangles)

# for each segment of the helix
    # generate a circle
    # position the circle
    # stitch the object

# generate a file

generator = Generator()
generator.print_model(obj)

