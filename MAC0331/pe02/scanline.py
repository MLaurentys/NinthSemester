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
from geocomp.lineintersections.rbtree import RBTree
from geocomp.lineintersections.node_types import *
from geocomp.lineintersections.segments_math import *

##############################
###
### PE 2 - START
###
##############################

#
# Makes the points the scanline is going to stop at
#

def make_event (hmap, heap, segment_nodes, point, position):
    #position 0: left -> segments_nodes = node
    #position 1: right -> segments_nodes = node
    #position -1: intersection -> segment_nodes = [node1, node2]
    if (point in hmap):
        node_event = hmap[point]
        node_event.add_to_segment(segment, position)
    else:
        new_event = Node_Event(point)
        new_event.add_to_segment(segment, position)
        heap.put(new_event)
        hmap[point] = new_event

# Makes initial map and queue of the segments limits
def make_event_points (node_segs):
    heap = queue.PriorityQueue()
    hmap = {}
    for ind in range(len(node_segs)):
        make_event (hmap, heap, node_segs[ind], node_segs[ind].start.get_point(), 0)
        make_event (hmap, heap, node_segs[ind], node_segs[ind].start.get_point(), 1)
    return heap, hmap

def make_segment_nodes (fixed_segments_array):
    nodes = []
    for i in range (len(fixed_segments_array)):
        nodes.append(Node_Seg(fixed_segments_array[i]))
    return nodes

##
## Scanline
##

def verify_n_intersection (n_seg, neigh, msg = ""):
    b_ret = False
    pt_ret = None
    if (neigh is None): return b_ret, pt_ret
    n_seg.seg.hilight(color_line="blue")
    neigh.hilight(color_line="blue")
    control.sleep()
    if (seg_intersects(n_seg.seg, neigh.seg)):
        int_point = intersection_locator(n_seg, neigh)
        control.plot_disc(int_point.coordinate[0], int_point.coordinate[1], "yellow", 6.0)
        #print("Enquanto comparava", seg, neigh)
        #print(msg, int_point.coordinate[0], int_point.coordinate[1])
        b_ret = True
        pt_ret =  int_point
    n_seg.seg.hilight(color_line="green")
    neigh.seg.hilight(color_line="green")
    return b_ret, pt_ret

def treat_left(s, bst):
    s.hilight(color_line="green")
    control.sleep()
    msg = "ACHOU INSERINDO:"
    new_intersections = []
    bst.insert(s)
    ns = bst.get_neighbours(s)
    ret1, pt1 = verify_n_intersection(s, ns[0], msg)
    if (ret1):
        new_intersections.append(pt1)
    ret2, pt2 = verify_n_intersection(s, ns[1], msg)
    if (ret2) :
        new_intersections.append(pt2)
    return ret1 or ret2, new_intersections

def treat_right (n_seg, bst):
    n_seg.seg.hilight(color_line="cyan")
    control.sleep()
    msg = "ACHOU REMOVENDO"
    new_intersections = []
    ret = False
    bst.remove(n_seg)
    ns = bst.get_neighbours(n_seg)
    if(ns[0] is not None and ns[1] is not None):
        ret, pt1 = verify_n_intersection(ns[0], ns[1], msg)
        if (ret): new_intersections.append(pt1)
    return ret, new_intersections

def treat_intersection (node_segs, bst, point):
    msg = "ACHOU OLHANDO INTERSECCAO"
    def define_pred(seg, ns):
        if ns[0] is not None:
            if not at_left(seg.init, seg.to, ns[0].init) \
                and not is_colinear(seg.init, seg.to, ns[0].init):
                return ns[0]
        if ns[1] is not None:
            if not at_left(seg.init, seg.to, ns[1].init) \
                and not is_colinear(seg.init, seg.to, ns[1].init):
                return ns[1]
        return None
    def define_suc(seg, ns):
        if ns[0] is not None:
            if at_left(seg.init, seg.to, ns[0].init):
                return ns[0]
        elif ns[1] is not None:
            if at_left(seg.init, seg.to, ns[1].init):
                return ns[1]
        return None
    new_intersections = []
    ret = ret1 = ret2 = False
    seg1 = node_segs[0]
    seg2 = node_segs[1]
    ns_1 = bst.get_neighbours(seg1)
    ns_2 = bst.get_neighbours(seg2)
    pred = define_pred(seg1, ns_1)
    suc = define_suc(seg2, ns_2)
    bst.remove(seg1)
    bst.remove(seg2)
    s1n.key = Node ((point[0], point[1] + 0.0001))
    s2n.key = Node ((point[0], point[1] - 0.0001))
    bst.insert(s2n)
    bst.insert(s1n)
    if pred is not None:
        pred.hilight(color_line="magenta")
        seg2.hilight(color_line="magenta")
        #print("Pred = ", pred, "Seg = ", seg2)
        control.sleep()
        ret1, pt1 = verify_n_intersection(seg2, pred, msg)
        if (ret1): new_intersections.append(pt1)
        pred.hilight(color_line="green")
        seg2.hilight(color_line="green")
    if suc is not None:
        #print("Suc = ", suc, "Seg = ", seg1)
        suc.hilight(color_line="magenta")
        seg1.hilight(color_line="magenta")
        control.sleep()
        ret2, pt2 = verify_n_intersection(seg1, suc, msg)
        if (ret2): new_intersections.append(pt2)
        suc.hilight(color_line="green")
        seg1.hilight(color_line="green")
    return ret1 or ret2, new_intersections


class intersection_locator:
    def __init__(self, seg1, seg2):
        self.coordinate = intersection(seg1.seg, seg2.seg)
        self.seg1 = seg1
        self.seg2 = seg2


# Scanline algorithm to find all intersections between segments in a plane
def Scanline (segments):
    fix_segments(segments)
    list_of_intersections = []
    segments = sorted(segments, key=functools.cmp_to_key(compare_segments))
    segments_nodes = make_segment_nodes(segments)
    heap, hmap = make_event_points(segments_nodes)
    bst = ABBB(node_ctor=Node_Seg)
    for i in range (len(segments)):
        segments[i].plot()
    while (not heap.empty()):
        #bst.print_tree()
        pt = heap.get()
        circ = control.plot_circle(pt.node.x, pt.node.y, "green", 2)
        control.sleep()
        # Start of a new segment
        for seg in pt.left:
            intersected, intersections = treat_left(segments[seg], bst)
            if(intersected):
                for inter in intersections:
                    make_event(hmap, heap, [inter.seg1, inter.seg2], inter.coordinate, -1)
                    list_of_intersections.append(inter)
        #End of an exhisting segment
        for seg in pt.right:
            intersected, intersections = treat_right(segments[seg], bst)
            if(intersected):
                for inter in intersections:
                    make_event(hmap, heap, [inter.seg1, inter.seg2], inter.coordinate, -1)
                    list_of_intersections.append(inter)
        #Intersections on the point (no specific order)
        for segs in pt.intersections:
            intersected, intersections = treat_intersection(segs, bst, pt.node.get_point())
            if(intersected):
                for inter in intersections:
                    make_event(hmap, heap, [inter.seg1, inter.seg2], inter.coordinate, -1)
                    list_of_intersections.append(inter)
        control.plot_delete(circ)
    print_aux2(list_of_intersections)
    return list_of_intersections

# auxiliary prints
def print_aux2(list_intersections):
    for inter in list_intersections:
        print("\n\n============")
        print("point = ", inter.coordinate)
        print("segment 1 = ", inter.seg1.seg)
        print("segment 2 = ", inter.seg2.seg)

def print_aux1(pt, segs):
    print(pt.node.x, pt.node.y)
    print("Ponto extremo dos segmentos:")
    for seg in pt.segments:
        print(segs[seg[0]])
    print("Ponto de interseccao entre os segmentos:")
    for inter in pt.intersections:
        print(inter[0], inter[1])
