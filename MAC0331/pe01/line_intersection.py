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

    

    def _get_neighbour(self, node):
        def find_left(start, node):
                ret = None
                if(start != None):
                    if (start < node):
                        temp = find_left(start.right, node)
                        ret = temp if (temp) else start
                    else:
                        ret = find_left(start.left, node)
                return ret
        def find_right(start, node):
            ret = None
            if(start != None):
                if (node < start):
                    temp = find_right(start.left, node)
                    ret = temp if(temp) else start
                else:
                    ret = find_right(start.right, node)
            return ret
        
        return find_left(self._root, node), find_right(self._root, node)

    def get_neighbours(self, val):
        nd = self._Node(val)
        ns = self._get_neighbour(nd)
        ns1 = ns[0].seg if(ns[0]) else None
        ns2 = ns[1].seg if(ns[1]) else None
        return ns1, ns2
##############################
###
### PE 1 - START
###
##############################

##
## Auxiliary functions for sorting
##

# order of segments is based on starting point only
def compare_segments(s1, s2):
    return compare_points(s1.init, s2.init)
# left before right, then bottom before top
def compare_points(pt1, pt2):
    if(pt1.x == pt2.x):
        return pt1.y - pt2.y
    return pt1.x - pt2.x

##
## Auxiliary function that does pre-processing
##

# Makes segment.start <= segment.end
def fix_segments (l):
    for i in range (len(l)):
        res = compare_points(l[i].init, l[i].to)
        if (res > 0):
            l[i].init, l[i].to = l[i].to, l[i].init
# Makes initial map and queue of the segments limits
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

##
## Functions reponsible for calculating intersections
##


def area2 (p1, p2, p3):
    return p1.x*p2.y - p1.y*p2.x + p1.y*p3.x \
            -p1.x*p3.y + p2.x*p3.y - p3.x*p2.y
def at_left(pt, p1, p2):
    return area2 (pt,p1,p2) > 0
def is_colinear (p1,p2,p3):
    return area2(p1,p2,p3) == 0
# Whether pt is in between p1 and p2 (presumes p1 <= p2)
def in_between(pt, p1, p2):
    ret = False
    if is_colinear(pt,p1,p2):
        if p1.x != p2.x:
            ret = p1.x <= pt.x <= p2.x
        else:
            ret = p1.y <= pt.y <= p2.y
    return ret

# Whether segmets cross in one midpoint
def seg_intersects_properly (seg1, seg2):
    a,b,c,d = seg1.init, seg1.to, seg2.init, seg2.to
    if is_colinear(a,c,d) or \
        is_colinear(b,c,d) or \
        is_colinear(c,a,b) or \
        is_colinear(d,a,b):
        return False
    return (at_left(a,c,d) != at_left(b,c,d)) and \
            (at_left(c,a,b) != at_left(d,a,b))

# Get intersection point
def intersection (seg1, seg2):
    def line(p1, p2):
        A = (p1.y - p2.y)
        B = (p2.x - p1.x)
        C = (p1.x*p2.y - p2.x*p1.y)
        return A, B, -C
    l1 = line(seg1.init, seg1.to)
    l2 = line(seg2.init, seg2.to)
    d = l1[0]*l2[1] - l1[1]*l2[0]
    dx = l1[2]*l2[1] - l1[1]*l2[2]
    dy = l1[0] * l2[2] - l1[2] * l2[0]
    x = dx/d
    y = dy/d
    return x,y

# Whether segments cross
def seg_intersects(seg1, seg2):
    a,b,c,d = seg1.init, seg1.to, seg2.init, seg2.to
    return prim.intersect(a,b,c,d)
    if (seg_intersects_properly(seg1, seg2)):
        return True
    return in_between(a,c,d) or in_between(b,c,d) or \
            in_between(c,a,b) or in_between(d,a,b)


##
## Scanline
##

def verify_n_intersection (seg, neigh, msg):
    if (not neigh): return False
    seg.hilight(color_line="blue")
    neigh.hilight(color_line="blue")
    if (seg_intersects(seg, neigh)):
        int_point = intersection(seg,neigh)
        control.plot_disc(int_point[0], int_point[1], "yellow", 6.0)
        print("Enquanto comparava", seg, neigh)
        print(msg, int_point[0], int_point[1])
        return True
    control.sleep()
    seg.hilight(color_line="green")
    neigh.hilight(color_line="green")

def treat_left(s, bst):
    msg = "ACHOU INSERINDO:"
    s.hilight(color_line="green")
    control.sleep()
    bst.insert(s)
    ns = bst.get_neighbours(s)
    ret = verify_n_intersection(s, ns[0], msg)
    if (ret) : return True
    ret = verify_n_intersection(s, ns[1], msg)
    if (ret) : return True

def treat_right (s, bst):
    msg = "ACHOU REMOVENDO:"
    ret = False
    s.hilight(color_line="cyan")
    control.sleep()
    bst.remove(s)
    ns = bst.get_neighbours(s)
    if(ns[0] and ns[1]):
        ret = verify_n_intersection(ns[0], ns[1], msg)
    return ret
    control.sleep()

# Scanline algorithm to find all intersections between segments in a plane
# Fixing typos
# highlight = segment.hilight
def Scanline (segments):
    fix_segments(segments)
    # should NEVER change the order of segments after sorted
    segments = sorted(segments, key=functools.cmp_to_key(compare_segments))
    heap, hmap = make_event_points(segments)
    bst = ABB(Node_Seg)
    for i in range (len(segments)):
        #print(str(i) +": " + str(segments[i]))
        segments[i].plot()
    
    while (not heap.empty()):
        pt = heap.get()
        circ = control.plot_circle(pt.node.x, pt.node.y, "green", 2)
        #print_aux1(pt, segments)
        control.sleep()
        if (len(pt.left) + len(pt.right) > 1):
            control.plot_disc(pt.node.x, pt.node.y, "yellow", 6.0)
            print("ACHOU IMEDIATAMENTE: no ponto ", pt.node.x, pt.node.y )
            return True
        # Start of a new segment
        for seg in pt.left:
            if(treat_left(segments[seg], bst)):
                return True
        #End of an exhisting segment
        for seg in pt.right:
            if(treat_right(segments[seg], bst)):
                return True

        #Intersections on the point (no specific order)
        for segs in pt.intersections:
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