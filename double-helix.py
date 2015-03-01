#!/usr/bin/python

import math
from mesh.generator import Generator
from mesh.shape_primitives import Circle
from mesh.object_model import ObjectModel
from mesh.shape_model import ShapeModel
from objects.tee_pipe import TeePipe

##################################################

obj = ObjectModel()

pipe1 = TeePipe(1)
pipe1.rotateY(math.pi)
pipe1.translate(5, 0, 0)

pipe2 = TeePipe(1)
pipe2.translate(-5, 0, 0)

obj.add_triangles(pipe1.get_triangles())
obj.add_triangles(pipe2.get_triangles())

# for each segment of the helix
    # generate a circle
    # position the circle
    # stitch the object

# generate a file

generator = Generator()
generator.print_model(obj)

