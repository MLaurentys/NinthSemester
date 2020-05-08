from geocomp.lineintersections.segments_math import at_left
from geocomp.lineintersections.rbtree import RBNode
# Used Node in PE02

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
        
    def get_point (self): return (self.x, self.y)

# Augmented 2D-point that carries information on its belonging
class Node_Event:
    def __init__(self, pt):
        super().__init__()
        self.node = Node(pt)
        self.segments = []
        # references to segment nodes
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
            self.add_to_intersection(seg[0], seg[1])
        else:
            print ("add_to_segment usage error. Ignoring...")

    def add_to_intersection(self, seg1, seg2):
        if (at_left(seg1.init, seg1.to, seg2.init)):
            self.intersections.add((seg1,seg2))
        elif (at_left(seg2.init, seg2.to, seg1.init)):
            self.intersections.add((seg2,seg1))
        elif (at_left(seg1.init, seg1.to, seg2.to)):
            self.intersections.add((seg1,seg2))
        elif (at_left(seg2.init, seg2.to, seg1.to)):
            self.intersections.add((seg2,seg1))
        else:
            print("major problem")

    def __lt__(self, other):
        return self.node < other.node

# Regular Node class to represent a 2D segment, based on its start and end positions
class Node_Seg:
    def __init__(self, seg):
        super().__init__()
        self.past_middle = False
        self.left = None
        self.right = None
        self.seg = seg
        self.start = Node(seg.init)
        self.end = Node(seg.to)
        self.key = self.start

    def get_val(self):
        return self.start, self.end, self.past_middle, self.seg

    def change_key (self, point):
        self.key = Node(point)

    def mark(self):
        self.mark = True

    def set_val(self, start, end, pm, seg):
        self.start = start
        self.end = end
        self.past_middle = pm
        self.seg = seg

    def __lt__(self, other):
        if (self.key.y < other.key.y):
            return True
        if other.key.y < self.key.y:
            return False
        if (self.key.x < other.key.x):
            return True
        return False

        s_comp_1 = self.start
        s_comp_2 = self.end
        o_comp_1 = other.start
        o_comp_2 = other.end
        if self.mark:
            s_comp_1 = self.end
            s_comp_2 = self.start
        if other.mark:
            o_comp_1 = other.end
            o_comp_2 = other.start

        if s_comp_1.y < o_comp_1.y:
            return True
        else:
            if (o_comp_1.y < s_comp_1.y):
                return False
            else:
                return s_comp_2.y < o_comp_2.y
