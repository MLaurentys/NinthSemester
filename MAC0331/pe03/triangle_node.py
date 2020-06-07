from random import shuffle
import networkx as nx
import matplotlib.pyplot as plt
from math import sqrt, ceil
from geocomp.common.point import Point
from geocomp.common.segment import Segment
from geocomp.common.prim import left, collinear, on_segment
from geocomp.common import control
from geocomp.common.prim import left

class Circle:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        p1 = (v1.x, v1.y);p2 = (v2.x, v2.y);p3 = (v3.x, v3.y)
        # Code from https://stackoverflow.com/questions/28910718/
        #   give-3-points-and-a-plot-circle
        temp = p2[0] * p2[0] + p2[1] * p2[1]
        bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
        cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
        det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

        # Center of circle
        cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
        cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

        radius = sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
        self.center = (cx, cy)
        self.radius = radius
        self.did = None

    def draw (self):
        if self.did is None:
            self.did = (control.plot_circle(self.center[0],\
                self.center[1], "#aa55ff", self.radius))
            for v in [self.v1, self.v2, self.v3]:
                v.hilight("#cc338b")

    def remove_draw (self):
        if self.did is not None:
            control.plot_delete(self.did)
            for v in [self.v1, self.v2, self.v3]:
                v.hilight("#00ffff")
            self.did = []

    def is_inside (self, p):
        d = sqrt(pow(self.center[0] - p.x, 2) +\
                 pow(self.center[1] - p.y, 2))
        return d < self.radius
class Node: #TRIANGLE in COUNTERCLOCKWISE order
    def __init__(self, x, y, z):
        if left(x, z, y): #makes sure triangle in in counter-clockwise
            temp = z
            z = y
            y = temp
        self.v1 = x
        self.v2 = y
        self.v3 = z
        self.d_ids = []

    def contains_proper (self, pt):
        return left(self.v1, self.v2, pt) and\
               left(self.v2, self.v3, pt) and\
               left(self.v3, self.v1, pt)

    def is_on_edge (self, pt):
        return on_segment(self.v1, self.v2, pt) or\
               on_segment(self.v2, self.v3, pt) or\
               on_segment(self.v3, self.v1, pt)

    def get_vertices(self): return (self.v1, self.v2, self.v3)

    def draw (self, col='#ffff00'):
        if (len(self.d_ids) > 0): return
        v1, v2, v3 = self.v1, self.v2, self.v3
        self.d_ids.append(control.plot_segment(v1.x, v1.y, v2.x, v2.y, color=col))
        self.d_ids.append(control.plot_segment(v2.x, v2.y, v3.x, v3.y, color=col))
        self.d_ids.append(control.plot_segment(v1.x, v1.y, v3.x, v3.y, color=col))

    def remove_draw (self):
        for dw in self.d_ids:
            control.plot_delete(dw)
        self.d_ids = []

    def get_edges (self):
        return (self.v1, self.v2),\
                (self.v2, self.v3),\
                (self.v3, self.v1)

    def get_relative_vertices (self, other):
        s1 = set(self.get_vertices())
        s2 = set(other.get_vertices())
        inter = s1.intersection(s2)
        dif = (s1.union(s2)) - inter
        return  inter, dif

    def needs_fix (self, other):
        # inter are the edges self and other have in common
        inter, dif = self.get_relative_vertices(other)
        # check if quad is convex
        if (len(inter) != 2 or len(dif) != 2):
            print("ERRO NA LEGALIZACAO")
            exit(1)
        if self.v1 in inter:
            if self.v2 in inter:
                inter_0 = self.v1
                inter_1 = self.v2
                dif_0 = self.v3
            else:
                inter_0 = self.v3
                inter_1 = self.v1
                dif_0 = self.v2
        else:
            inter_0 = self.v2
            inter_1 = self.v3
            dif_0 = self.v1
        if other.v1 in inter:
            if other.v2 in inter:
                dif_1 = other.v3
            else:
                dif_1 = other.v2
        else:
            dif_1 = other.v1

        if not left(inter_0, inter_1, dif_1):
            aux = dif_0
            dif_0 = dif_1
            dif_1 = aux
        convex = left(inter_0, dif_0, inter_1) and\
                 left(dif_0, inter_1, dif_1) and\
                 left(inter_1, dif_1, inter_0) and\
                 left(dif_1, inter_0, dif_0)

        if not convex: return False
        # check if inter is best
        # only draws if passes convex
        self.draw("#ffaa33")
        other.draw("#ffaa33")
        did = control.plot_segment(inter_0.x, inter_0.y, inter_1.x,\
                                   inter_1.y, color="#ffffff")
        control.sleep()
        control.plot_delete(did)
        self.remove_draw()
        other.remove_draw()

        C = Circle(inter_0, inter_1, dif_0)
        C.draw()
        control.sleep()
        C.remove_draw()
        return C.is_inside(dif_1)
