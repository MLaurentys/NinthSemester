#!/usr/bin/env python
"""Scanline algorithm for line intersections"""
import queue
import functools
from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config
from geocomp import colors

# Data Structure I Implemented

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

    def add_to_segment(self, seg, pos):
        self.segments.append((seg,pos))
        if(pos == 0):
            self.left.append(seg)
        else:
            self.right.append(seg)

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
        self.start = Node(seg[0])
        self.end = Node(seg[1])

    def get_val(self):
        return self.start, self.end

    def set_val(self, start, end):
        self.start = start
        self.end = end

    def __lt__(self, other):
        return self.start < other.start

# BST data structure that should work for any comparable (class that implements __lt__)
class ABB:
    def __init__(self, Nd_constr):
        super().__init__()
        self._root = None
        self._Node = Nd_constr

    def insert(self, val):
        nd = self._Node(val)
        if (self._root == None):
            self._root = nd
            return
        node = self._root
        par = None
        while (node):
            par = node
            if (nd < node):
                node = node.left
            else:
                node = node.right
        if (nd < par):
            par.left = nd
        else:
            par.right = nd

    def _remove(self, cur_node, node):
        if (cur_node is None):
            return None
        if (node < cur_node):
            cur_node.left = self._remove(cur_node.left, node)
        elif (cur_node < node):
            cur_node.right = self._remove(cur_node.right, node)
        else:
            if (cur_node.left is None):
                ret = cur_node.right
                cur_node = None
                return ret
            elif (cur_node.right is None):
                ret = cur_node.left
                cur_node = None
                return ret
            else:
                n_node = self.get_min(cur_node.right)
                s,e = n_node.get_val()
                cur_node.set_val(s,e)
                cur_node.right = self._remove(cur_node.right, n_node)
        return cur_node


    def remove(self, val):
        nd = self._Node(val)
        self._root = self._remove(self._root, nd)

    def get_min(self, node):
        par = None
        nd = node
        while (nd):
            par = nd
            nd = nd.left
        return par

    def is_empty(self):
        return self._root == None



# PE 1 - START

def compare_segments(s1, s2):
    return compare_points(s1.init, s2.init)
def compare_points(pt1, pt2):
    if(pt1.x == pt2.x):
        return pt1.y - pt2.y
    return pt1.x - pt2.x

# init = esquerdo, to = direito
def fix_segments (l):
    for i in range (len(l)):
        res = compare_points(l[i].init, l[i].to)
        if (res > 0):
            l[i].init, l[i].to = l[i].to, l[i].init
def make_event_points (segs):
    heap = queue.PriorityQueue()
    hmap = {}
    for ind in range(len(segs)):
        if segs[ind].init in hmap:
            hi = hmap[segs[ind].init]
            hi.add_to_segment(ind, 0)
        else:
            nd_i = Node_Event(segs[ind].init)
            nd_i.add_to_segment(ind, 0)
            heap.put(nd_i)
            hmap[segs[ind].init] = nd_i
        if segs[ind].to in hmap:
            ht = hmap[segs[ind].to]
            ht.add_to_segment(ind, 1)
        else:
            nd_t = Node_Event(segs[ind].to)
            nd_t.add_to_segment(ind, 1)
            heap.put(nd_t)
            hmap[segs[ind].to] = nd_t
    return heap, hmap

# Scanline algorithm to find all intersections between segments in a plane
def Scanline (segments):
    print(type(segment))
    fix_segments(segments)
    print(segments)
    # should NEVER change the order of segments after sorted
    segments = sorted(segments, key=functools.cmp_to_key(compare_segments))
    heap, hmap = make_event_points(segments)

    # for i in range (len(segments)):
    #     print(str(i) +": " + str(segments[i]))
    #     segments[i].plot()
    
    while (not heap.empty()):
        pt = heap.get()
        print_aux1(pt, segments)
        # Start of a new segment
        for seg in pt.left:
            circ = control.plot_circle(pt.node.x, pt.node.y, "green", 2)
            segments[seg].highlight
            control.sleep()

            control.plot_delete(circ)
        #End of an exhisting segment
        for seg in pt.right:
            circ = control.plot_circle(pt.node.x, pt.node.y, "yellow", 2)
            control.sleep()

            control.plot_delete(circ)
        #Intersections on the point (no specific order)
        for segs in pt.intersections:
            circ = control.plot_circle(pt.node.x, pt.node.y, "red", 2)
            control.sleep()

            control.plot_delete(circ)

# auxiliary prints
def print_aux1(pt, segs):
    print(pt.node.x, pt.node.y)
    print("Ponto extremo dos segmentos:")
    for seg in pt.segments:
        print(segs[seg[0]])
    print("Ponto de interseccao entre os segmentos:")
    for inter in pt.intersections:
        print(inter[0], inter[1])