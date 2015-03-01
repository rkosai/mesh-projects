import copy
import math

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
        for i in range(len(self.vectors)):
            self.vectors[i][0] += dx
            self.vectors[i][1] += dy
            self.vectors[i][2] += dz

    def _rotateVector(self, theta, index_1, index_2):
        for i in range(len(self.vectors)):
            j = self.vectors[i][index_1]
            k = self.vectors[i][index_2]
            radius = math.sqrt(math.pow(j, 2) + math.pow(k, 2))
            angle = math.atan2(k, j)

            self.vectors[i][index_1] = radius * math.cos(angle - theta)
            self.vectors[i][index_2] = radius * math.sin(angle - theta)

    def rotateY(self, theta):
        self._rotateVector(theta, 0, 2)

    def rotateX(self, theta):
        self._rotateVector(theta, 2, 1)

    def rotateZ(self, theta):
        self._rotateVector(theta, 1, 0)

    def get_triangles(self):
        return self.triangles

    def get_edges(self):
        return self.edges

    def get_vectors(self):
        return self.vectors
