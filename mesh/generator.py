class Generator:

    def __init__(self):
        self.scale = 1;

    def set_scale(self, scale):
        self.scale = scale;

    def print_model(self, model):
        print "solid demo"

        def _scale(l):
            return tuple([x * self.scale for x in l])

        for t in model.get_mesh():
            print "facet normal %e %e %e" % (0, 0, 0)
            print"outer loop"
            print "vertex %e %e %e" % _scale(t[0])
            print "vertex %e %e %e" % _scale(t[1])
            print "vertex %e %e %e" % _scale(t[2])
            print "endloop"
            print "endfacet"

        print "endsolid demo"
