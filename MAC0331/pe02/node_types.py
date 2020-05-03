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
        self.left = []  #int ID
        self.right = [] #int ID
        self.intersections = set() #segs by value

    def add_to_segment(self, seg, identifier):
        self.segments.append((seg, identifier))
        if(identifier == 0):
            self.left.append(seg)
        elif (identifier == 1):
            self.right.append(seg)
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

    def get_val(self):
        return self.start, self.end

    def mark(self):
        self.mark = True

    def set_val(self, start, end):
        self.start = start
        self.end = end

    def __lt__(self, other):
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

    # def cheat_comparison(self, other):
    #     if self.end.y < other.end.y:
    #         return True
    #     else:
    #         if (other.end.y < self.end.y):
    #             return False
    #         else:
    #             return self.start.y < other.start.y