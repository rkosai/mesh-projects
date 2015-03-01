import math

class MeshUtils:

    @staticmethod
    def stitch_shapes(s1, s2):
        if (s1 is None) or (s2 is None):
            print "#ERROR: Can't merge empty shape."

        # stitch shapes together
        triangles = []
        edge_pool = s1.get_edges() + s2.get_edges()

        # create a new edge joining two shapes
        current_edge = MeshUtils._get_closest_vertices(s1, s2)

        # stitch the shapes together with triangles
        while len(edge_pool) > 0:
            current_edge = MeshUtils._form_triangle(
                triangles, s1, current_edge, edge_pool)

        return triangles

    @staticmethod
    def _form_triangle(triangles, s1, current_edge, pool):
        # find all the possible edges we can use for a triangle
        possible_edges = []
        for i in range(len(pool)):
            e1 = current_edge
            e2 = pool[i]

            uv_current, uv_candidate = (None, None)

            # find the common vertex,and the "unattached vertex"
            if e1[0] == e2[0]:
                uv_current, uv_candidate = (1, 1)
            elif e1[0] == e2[1]:
                uv_current, uv_candidate = (1, 0)
            elif e1[1] == e2[0]:
                uv_current, uv_candidate = (0, 1)
            elif e1[1] == e2[1]:
                uv_current, uv_candidate = (0, 0)

            if uv_current is not None:
                possible_edges.append(
                    (i, e1[uv_current], e2[uv_candidate])
                )

        # find the shortest edge to connect to
        shortest_distance = float("inf")
        shortest_tuple = None

        # Find the candidate vertex that is closest to the current edge
        for etuple in possible_edges:
            index, uv_current, uv_candidate = etuple
            distance = math.sqrt(
                math.pow(current_edge[0][0] - uv_candidate[0], 2) +
                math.pow(current_edge[0][1] - uv_candidate[1], 2) +
                math.pow(current_edge[0][2] - uv_candidate[2], 2) +
                math.pow(current_edge[1][0] - uv_candidate[0], 2) +
                math.pow(current_edge[1][1] - uv_candidate[1], 2) +
                math.pow(current_edge[1][2] - uv_candidate[2], 2)
            )

            if distance < shortest_distance:
                shortest_tuple = etuple
                shortest_distance = distance

        # Make the triangle, remove the used edges from the pool, and
        # return the newly formed edge to build off of.
        if shortest_tuple is None:
            return None
        else:
            index, uv_current, uv_candidate = shortest_tuple
            triangles.append(
                (current_edge[0], current_edge[1], uv_candidate)
            )

            pool.pop(index)

            # return edge in shape-one, shape-two order
            if uv_current in s1.get_vectors():
                return (uv_current, uv_candidate)
            else:
                return (uv_candidate, uv_current)

    @staticmethod
    def _get_closest_vertices(shape1, shape2):
        edges_1 = shape1.get_edges()
        edges_2 = shape2.get_edges()

        closest_vertices = None
        closest_distance = float("inf")
        for e1 in edges_1:
            for e2 in edges_2:
                xyz1 = e1[0]
                xyz2 = e2[0]
                distance = math.sqrt(
                    math.pow(xyz1[0] - xyz2[0], 2) +
                    math.pow(xyz1[1] - xyz2[1], 2) +
                    math.pow(xyz1[2] - xyz2[2], 2)
                )
                if distance < closest_distance:
                    closest_vertices = (e1[0], e2[0])
                    closest_distance = distance

        return closest_vertices

    @staticmethod
    def translate_v(vector, dx, dy, dz):
        x = vector[0] + dx
        y = vector[1] + dy
        z = vector[2] + dz

        return (x, y, z)

    @staticmethod
    def rotatev(vector, theta, index_1, index_2):
        new_vector = [vector[0], vector[1], vector[2]]

        j = vector[index_1]
        k = vector[index_2]
        radius = math.sqrt(math.pow(j, 2) + math.pow(k, 2))
        angle = math.atan2(k, j)

        new_vector[index_1] = radius * math.cos(angle - theta)
        new_vector[index_2] = radius * math.sin(angle - theta)

        return (new_vector[0], new_vector[1], new_vector[2])

    @staticmethod
    def rotatev_x(vector, theta):
        return MeshUtils.rotatev(vector, theta, 2, 1)

    @staticmethod
    def rotatev_y(vector, theta):
        return MeshUtils.rotatev(vector, theta, 0, 2)

    @staticmethod
    def rotatev_z(vector, theta):
        return MeshUtils.rotatev(vector, theta, 1, 0)

