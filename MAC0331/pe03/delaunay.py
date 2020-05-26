from random import shuffle
import networkx as nx
from geocomp.common.point import Point
from geocomp.common.segment import Segment
from geocomp.common.prim import left
from geocomp.common import control
root = None
DG = None

class Point: #Point in 2D
    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def is_inside (self, nd):
        pass

class Node: #TRIANGLE in COUNTERCLOCKWISE order
    def __init__(self, x, y, z):
        self.v1 = x
        self.v2 = y
        self.v3 = z
        self.d_ids = []

    def contains (self, pt):
        return left(self.v1, self.v2, pt) and\
               left(self.v2, self.v3, pt) and\
               left(self.v3, self.v1, pt)

    def get_vertices(self): return (self.v1, self.v2, self.v3)

    def draw (self):
        v1, v2, v3 = self.v1, self.v2, self.v3
        self.d_ids.append(control.plot_segment(v1.x, v1.y, v2.x, v2.y, color='#ffff00'))
        self.d_ids.append(control.plot_segment(v2.x, v2.y, v3.x, v3.y, color='#ffff00'))
        self.d_ids.append(control.plot_segment(v1.x, v1.y, v3.x, v3.y, color='#ffff00'))
        control.sleep()

    def remove_draw(self):
        for dw in self.d_ids:
            control.plot_delete(dw)
        self.d_ids = []

def add_to (p1, p2, p3, par):
    global DG
    t = Node(p1,p2,p3)
    DG.add_node(t)
    if par is not None:
        DG.add_edge(par, t)
    return t

def find_destine(pt):
    global DG, root
    visited = set()
    stack = [root]
    visited.add(root)
    while (True):
        node = stack.pop()
        if not node.contains(pt):
            continue

        pass
    return node

def pre_process (points):
    global DG, root
    shuffle(points)
    inside = []
    not_inside = [i for i in range(len(points))]
    min_x = min_y = float('inf')
    max_x = max_y = -float('inf')
    for pt in points:
        if pt.x < min_x: min_x = pt.x
        if pt.x > max_x: max_x = pt.x
        if pt.y > max_y: max_y = pt.y
        if pt.y < min_y: min_y = pt.y
    mid_hor = (max_x + min_x) / 2.0  #fixed
    left_hor = mid_hor - (max_x - min_x) * 0.75 #fixed
    hor_fact = (max_x - min_x) #variable
    mid_ver = (max_y + min_y) / 2.0  #fixed
    len_ver = (max_y - min_y)        #variable
    node = None
    while (len(not_inside) > 0):
        node = Node(Point(left_hor, mid_ver + len_ver),
                    Point(left_hor, mid_ver - len_ver),
                    Point(mid_hor + hor_fact, mid_ver))
        for i in range(len(not_inside)):
            if node.contains(points[not_inside[i]]):
                inside.append(i)
        for ind in reversed(inside):
            not_inside.pop(ind)
        inside = []
        hor_fact *= 1.15
        len_ver *= 1.5
    DG = nx.DiGraph()
    root = node
    DG.add_node(root)

def triangulation (points):
    global DG, root

    pre_process(points)
    root.draw()
    root.remove_draw()
    # for pt in points:
    #     find_destine(pt)
    #     # encontra onde pt esta em DG
    #     # Adiciona pt e as tres novas arestas
    #     #legaliza as arestas de DG
    #     #adi
    #     break
    #     pass

