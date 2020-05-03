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

# Augmented 2D-point that carries information on its belonging
class Node_Event:
    def __init__(self, pt):
        super().__init__()
        self.node = Node(pt)
        self.segments = []
        self.left = []
        self.right = []
        self.intersections = set()

    def add_to_segment(self, seg, identifiers):
        self.segments.append((seg,identifiers))
        if(identifiers == 0):
            self.left.append(seg)
        elif (identifiers == 1):
            self.right.append(seg)
        elif (identifiers == -1):
            self.add_to_intersection(seg[0], seg[1])
        else:
            print ("add_to_segment usage error. Ignoring...")

    def add_to_intersection(self, seg1, seg2):
        self.intersections.add((seg1,seg2))

    def __lt__(self, other):
        return self.node < other.node

# Regular Node class to represent a 2D segment, based on its start and end positions
class Node_Seg:
    def __init__(self, seg):
        super().__init__()
        self.left = None
        self.right = None
        self.seg = seg
        self.start = Node(seg.init)
        self.end = Node(seg.to)

    def get_val(self):
        return self.start, self.end

    def set_val(self, start, end):
        self.start = start
        self.end = end

    def __lt__(self, other):
        if self.start.y < other.start.y:
            return True
        else:
            if (other.start.y < self.start.y):
                return False
            else:
                return self.end.y < other.end.y
