
# twin is implicit -> he[v1][v2].twin = he[v2][v1]
class hedge:
    def __init__(self, v1, v2, face=None, prev=None, nxt=None):
        self.origin = v1
        self.destine = v2
        self.twin = None
        self.prev = prev
        self.next = nxt
        self.face = face #triangle node!

    def get_points(self): return (self.origin, self.destine)

    def set_data(self, face=None, prev=None, nxt=None):
        if face is not None:
            self.face = face
        if prev is not None:
            self.prev = prev
        if nxt is not None:
            self.next = nxt

class DCEL:
    def __init__(self):
        self.hedges = {}

    def add_hedge(self, hedge):
        points_tuple = hedge.get_points()
        self.hedges[points_tuple] = hedge

    def get_hedge(self, points_tuple):
        if points_tuple not in self.hedges:
            print ("FATAL ERROR! EDGE NOT PRESENT")
        return self.hedges[points_tuple]

    def remove_edge(self, point1, point2, simple=False):
        if simple:
            self.hedges.pop((point1, point2), None)
            self.hedges.pop((point2, point1), None)
            return
        h1 = self.hedges.pop((point1, point2), None)
        h2 = self.hedges.pop((point2, point1), None)
        if h1 is None or h2 is None:
            print("Erro fatal removendo")
        h1.prev.next = h2.next
        h2.next.prev = h1.prev
        h1.next.prev = h2.prev
        h2.prev.next = h1.next
        h1.twin = None
        h2.twin = None

    def get_twin(self, hedge):
        return self.hedges[(hedge.destine, hedge.origin)]