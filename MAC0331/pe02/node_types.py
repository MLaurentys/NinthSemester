from geocomp.lineintersections.segments_math import at_left

# Used Node in PE02

# Regular Node Class that represents a point in 2D-space
class Node:
    def __init__(self, pt):
        super().__init__()
        self.left = None
        self.right = None
        self.x = pt[0]
        self.y = pt[1]

    def get_pt(self): return (self.x, self.y)

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
        self.left = set()  #int ID
        self.right = set() #int ID
        self.intersections = set() #int ID

    def get_coordinate(self): return self.node.get_pt()

    def add_to_segment(self, seg, identifier):
        if(identifier == 0):
            self.left.add(seg)
        elif (identifier == 1):
            self.right.add(seg)
        elif (identifier == -1):
            self.intersections.add(seg)
        else:
            print ("add_to_segment usage error. Ignoring...")

    def __lt__(self, other):
        return self.node < other.node

# Regular Node class to represent a 2D segment
class Node_Seg:
    def __init__(self, seg, k):
        super().__init__()
        self.value = seg
        self.key = k

    def __lt__(self, other):
        a = 0
        if self.value.has_left(other.key):return True
        if other.value.has_left(self.key):return False
        if self.value.has_left(other.value.to): return True
        return False