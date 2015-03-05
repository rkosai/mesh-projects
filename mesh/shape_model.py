import copy
import math
from shape_utils import ShapeUtils

class ShapeModel():
    def __init__(self):
        self.vectors = []
        self.edges = []
        self.triangles = []

        self.previous_vector = None

    def add_vector(self, x, y, z):
        vector = [x, y, z]
        self.vectors.append(vector)

        if (self.previous_vector is not None):
            edge = (self.previous_vector, vector)
            self.edges.append(edge)

        self.previous_vector = vector

    def close_vectors(self):
        if self.previous_vector is None:
            print "#ERROR: No previous vector to close."
            return

        elif len(self.vectors) == 0:
            print "#ERROR: Can't close an empty shape."
            return

        edge = (self.previous_vector, self.vectors[0])
        self.edges.append(edge)

    def fill_internal_edges(self):
        edges = copy.copy(self.edges)

        # find adjacent edges and make triangles
        while len(edges) > 3:
            e1 = edges.pop(0)
            e2 = edges.pop(0)
            e3 = (e1[0], e2[1])
            edges.insert(0, e3)

            triangle = (e1[0], e2[0], e2[1])
            self.triangles.append(triangle)

        # when an edge == 3, then that's the last triangle
        if len(edges) == 3:
            triangle = (edges[0][0], edges[1][0], edges[2][0])
            self.triangles.append(triangle)

    def translate(self, dx, dy, dz):
        for v in self.vectors:
            v[0], v[1], v[2] = ShapeUtils.translate_v(v, dx, dy, dz)

    def rotateX(self, theta):
        for v in self.vectors:
            v[0], v[1], v[2] = ShapeUtils.rotatev_x(v, theta)

    def rotateY(self, theta):
        for v in self.vectors:
            v[0], v[1], v[2] = ShapeUtils.rotatev_y(v, theta)

    def rotateZ(self, theta):
        for v in self.vectors:
            v[0], v[1], v[2] = ShapeUtils.rotatev_z(v, theta)

    def get_triangles(self):
        return self.triangles

    def get_edges(self):
        return self.edges

    def get_vectors(self):
        return self.vectors

    def reverse_edges(self):
        new_edges = []
        for edge in reversed(self.edges):
            p1, p2 = edge
            new_edges.append([p2, p1])

        self.edges = new_edges
