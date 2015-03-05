class ObjectModel:
    def __init__(self):
        self.triangles = []

    def add_triangles(self, t):
        self.triangles += t

    def get_triangles(self):
        return self.triangles

    def set_triangles(self, triangles):
        self.triangles = triangles
