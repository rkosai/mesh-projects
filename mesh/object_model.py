class ObjectModel:
    def __init__(self):
        self.triangles = []

    def add_mesh(self, t):
        self.triangles += t

    def get_mesh(self):
        return self.triangles

    def set_mesh(self, triangles):
        self.triangles = triangles

    def apply_transform(self, function, params):
        new_triangles = function(self.triangles, *params)
        self.triangles = new_triangles
