from geocomp.common.prim import left as at_left
from geocomp.common.point import Point
# Regular Node Class that represents a point in 2D-space
class Node:
    def __init__(self, pt):
        super().__init__()
        self.left = None
        self.right = None
        self.x = pt[0]
        self.y = pt[1]

    def __lt__(self, other):
        if (self.x == other.x):
            return self.y < other.y
        else:
            return self.x < other.x
        
    def get_point (self): return Point(self.x, self.y)

# Augmented 2D-point that carries information on its belonging
class Node_Event:
    def __init__(self, pt):
        super().__init__()
        self.node = Node(pt)
        self.segments = []
        self.left = set()
        self.right = set()
        self.intersections = set()

    def add_to_segment(self, seg, identifier):
        self.segments.append((seg, identifier))
        if(identifier == 0):
            self.left.add(seg)
        elif (identifier == 1):
            self.right.add(seg)
        elif (identifier == -1):
            self.intersections.add(seg[0])
            self.intersections.add(seg[1])
            #self.add_to_intersection(seg[0], seg[1])
        else:
            print ("add_to_segment usage error. Ignoring...")

    def add_to_intersection(self, seg1, seg2):
        if (at_left(seg1.init, seg1.to, seg2.init)):
            self.intersections.add((seg1,seg2))
        elif (at_left(seg2.init, seg2.to, seg1.init)):
            self.intersections.add((seg2,seg1))
        elif (at_left(seg1.init, seg1.to, seg2.to)):
            self.intersections.add((seg2,seg1))
        elif (at_left(seg2.init, seg2.to, seg1.to)):
            self.intersections.add((seg1,seg2))
        else:
            print("major problem")

    def __lt__(self, other):
        return self.node < other.node

# Regular Node class to represent a 2D segment, based on its start and end positions
class Node_Seg:
    def __init__(self, seg):
        super().__init__()
        self.left = None
        self.right = None
        self.seg = seg

    def get_val (self):
        return self.seg

    def set_val (self, seg):
        self.seg = seg

    def __lt__(self, other):
        # Is this.key ABOVE this.key?
        # 
        if (self.key.y < other.key.y):
            return False
        if other.key.y < self.key.y:
            return True
        if (self.key.x < other.key.x):
            return False
        if (other.key.x < self.key.x):
            return True
        if (self.end.y < other.end.y):
            return False
        if other.end.y < self.end.y:
            return True
        if (self.end.x < other.end.x):
            return False
        return False
