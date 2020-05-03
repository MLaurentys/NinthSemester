#!/usr/bin/env python
"""Scanline algorithm for line intersections"""
import queue
import functools
from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config
from geocomp import colors
from geocomp.lineintersections.ABBB import ABBB
from geocomp.lineintersections.node_types import *
from geocomp.lineintersections.segments_math import *

##############################
###
### PE 2 - START
###
##############################

##
## Auxiliary function that does pre-processing
##

# order of segments is based on starting point only
def compare_segments(s1, s2):
    return compare_points(s1.init, s2.init)

# left before right, then bottom before top
def compare_points(pt1, pt2):
    if(pt1.x == pt2.x):
        return pt1.y - pt2.y
    return pt1.x - pt2.x

# Makes segment.start <= segment.end
def fix_segments (l):
    for i in range (len(l)):
        res = compare_points(l[i].init, l[i].to)
        if (res > 0):
            l[i].init, l[i].to = l[i].to, l[i].init

def make_event (hmap, heap, segment, point, position):
    #position 0: left
    #position 1: right
    #position -1: intersection -> segment = [seg1, seg2]
    if (point in hmap):
        node_event = hmap[point]
        node_event.add_to_segment(segment, position)
    else:
        new_event = Node_Event(point)
        new_event.add_to_segment(segment, position)
        heap.put(new_event)
        hmap[point] = new_event
# Makes initial map and queue of the segments limits
def make_event_points (segs):
    heap = queue.PriorityQueue()
    hmap = {}
    for ind in range(len(segs)):
        make_event (hmap, heap, segs[ind], segs[ind].init, 0)
        make_event (hmap, heap, segs[ind], segs[ind].to, 1)
    return heap, hmap


##
## Scanline
##

def verify_n_intersection (seg, neigh, msg):
    if (not neigh): return False, None
    seg.hilight(color_line="blue")
    neigh.hilight(color_line="blue")
    if (seg_intersects(seg, neigh)):
        int_point = intersection_locator(seg, neigh)
        control.plot_disc(int_point[0], int_point[1], "yellow", 6.0)
        print("Enquanto comparava", seg, neigh)
        print(msg, int_point[0], int_point[1])
        return True, int_point
    control.sleep()
    seg.hilight(color_line="green")
    neigh.hilight(color_line="green")
    return False, None

def treat_left(s, bst):
    msg = "ACHOU INSERINDO:"
    new_intersections = []
    s.hilight(color_line="green")
    control.sleep()
    bst.insert(s)
    ns = bst.get_neighbours(s)
    ret1, seg1 = verify_n_intersection(s, ns[0], msg)
    if (ret1):
        new_intersections.append(seg1)
    ret2, seg2 = verify_n_intersection(s, ns[1], msg)
    if (ret2) :
        new_intersections.append(seg2)
    return ret1 or ret2, new_intersections

def treat_right (s, bst):
    msg = "ACHOU REMOVENDO"
    ret = False
    s.hilight(color_line="cyan")
    control.sleep()
    bst.remove(s)
    ns = bst.get_neighbours(s)
    if(ns[0] and ns[1]):
        ret = verify_n_intersection(ns[0], ns[1], msg)
    return ret
    control.sleep()

class intersection_locator:
    def __init__(self, seg1, seg2):
        self.coordinate = intersection(seg1, seg2)
        self.seg1 = seg1
        self.seg2 = seg2


# Scanline algorithm to find all intersections between segments in a plane
def Scanline (segments):
    fix_segments(segments)
    list_of_intersections = []
    segments = sorted(segments, key=functools.cmp_to_key(compare_segments))
    heap, hmap = make_event_points(segments)
    bst = ABBB(Node_Seg)
    for i in range (len(segments)):
        segments[i].plot()
    
    while (not heap.empty()):
        pt = heap.get()
        circ = control.plot_circle(pt.node.x, pt.node.y, "green", 2)
        #print_aux1(pt, segments)
        control.sleep()
        if (len(pt.left) + len(pt.right) > 1):
            control.plot_disc(pt.node.x, pt.node.y, "yellow", 6.0)
            print("ACHOU IMEDIATAMENTE: no ponto ", pt.node.x, pt.node.y )
        # Start of a new segment
        for seg in pt.left:
            intersected, intersections = treat_left(segments[seg], bst)
            if(intersected):
                for inter in intersection:
                    if(inter not in hmap):
                        list_of_intersections.append(inter)
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