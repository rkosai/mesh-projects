#!/usr/bin/python

from mesh.generator import Generator
from mesh.shape_primitives import Circle
from mesh.object_model import ObjectModel
from mesh.shape_model import ShapeModel
from objects.tee_pipe import TeePipe

##################################################

obj = ObjectModel()

pipe = TeePipe(1)
obj.add_triangles(pipe.get_triangles())

# for each segment of the helix
    # generate a circle
    # position the circle
    # stitch the object

# generate a file

generator = Generator()
generator.print_model(obj)

