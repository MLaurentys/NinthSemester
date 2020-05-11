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
from geocomp.lineintersections.rbtree import RBTree
from numpy import argsort
from geocomp.common.point import Point
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

def make_event (hmap, heap, segments, point, position):
    #position 0: left
    #position 1: right
    #position -1: intersection
    if (point in hmap):
        node_event = hmap[point]
    else:
        node_event = Node_Event(point)
        heap.put(node_event)
        hmap[point] = node_event
    for seg in segments:
        node_event.add_to_segment(seg, position)

# Makes initial map and queue of the segments limits
def make_event_points (segs):
    heap = queue.PriorityQueue()
    hmap = {}
    for ind in range(len(segs)):
        make_event (hmap, heap, [ind], segs[ind].init, 0)
        make_event (hmap, heap, [ind], segs[ind].to, 1)
    return heap, hmap


##
## Scanline
##

def verify_n_intersection (seg, neigh, seg_map, msg = ""):
    b_ret = False
    pt_ret = None
    if (neigh is None): return b_ret, pt_ret
    control.sleep()
    if (seg_intersects(seg, neigh)):
        int_point = intersection_locator(seg1=seg, seg2=neigh,\
                        seg1_ind=seg_map[seg], seg2_ind=seg_map[neigh])
        print("Enquanto comparava", seg, neigh)
        print(msg, int_point.coordinate[0], int_point.coordinate[1])
        b_ret = True
        pt_ret =  int_point
    return b_ret, pt_ret

def treat_left(seg_ind, segs, keys, seg_map, bst):
    s = segs[seg_ind]
    k = keys[seg_ind]
    s.hilight(color_line="green")
    msg = "ACHOU INSERINDO:"
    new_intersections = []
    bst.insert(keys[seg_ind], s)
    control.sleep()
    s.hilight(color_line="blue")
    prev, succ = bst.get_neighbours(k)
    for p in [prev, succ]:
        if p[0] is not None:
            if p[1] == s: 
                continue
            p[1].hilight(color_line="blue")
            ret1, pt1 = verify_n_intersection(s, p[1], seg_map, msg)
            if (ret1):
                new_intersections.append(pt1)
            p[1].hilight(color_line="green")
    s.hilight(color_line="green")
    return len(new_intersections) != 0, new_intersections

def treat_right (seg_ind, segs, keys, seg_map, bst):
    s = segs[seg_ind]
    k = keys[seg_ind]
    s.hilight(color_line="cyan")
    control.sleep()
    msg = "ACHOU REMOVENDO"
    new_intersections = []
    ret = False
    prev, succ = bst.get_neighbours(k)
    bst.remove(k)
    if(prev[0] is not None and succ[0] is not None):
        prev[1].hilight(color_line="blue")
        succ[1].hilight(color_line="blue")
        control.sleep()
        ret, inter_locator =\
            verify_n_intersection(prev[1], succ[1], seg_map, msg)
        if (ret): new_intersections.append(inter_locator)
        prev[1].hilight(color_line="green")
        succ[1].hilight(color_line="green")
    return ret, new_intersections

def treat_intersection (coordinate, list_ind, segs, keys, seg_map, bst):
    if len(list_ind) == 0: return False, None
    L = len(list_ind)
    list_ind = list(list_ind) #set to list
    msg = "ACHOU OLHANDO INTERSECCAO"
    new_intersections = []
    list_segs = [None for i in range (len(list_ind))]
    for i in range(len(list_ind)):
        if bst.get_value(keys[list_ind[i]]) is not None:
            bst.remove(keys[list_ind[i]])
    for i in range(len(list_segs)):
        keys[list_ind[i]] = Point(coordinate[0],\
                            coordinate[1])
        list_segs[i] = Node_Seg(segs[list_ind[i]], keys[list_ind[i]])
    list_ord = argsort(list_segs)
    for i in range(len(list_segs)):
        keys[list_ind[i]] = Point(coordinate[0],\
                            coordinate[1] + list_ord[i] * 0.1)
    bst.insert (keys[list_ind[0]], segs[list_ind[0]]) #could be any term
    prev, succ = bst.get_neighbours(keys[list_ind[0]])
    bst.remove (keys[list_ind[0]])
    for p in [prev, succ]:
        if p[0] is not None:
            val = p[1]
            ind = seg_map[val]
            val.hilight(color_line="magenta")
            for ind in list_ind:
                seg = segs[ind]
                seg.hilight(color_line="magenta")
                ret, inter_locate = verify_n_intersection(\
                                        seg, val, seg_map, msg)
                if ret: new_intersections.append(inter_locate)
                control.sleep()
                seg.hilight(color_line="green")
            val.hilight(color_line="green")
    return len(new_intersections) != 0, new_intersections


class intersection_locator:
    def __init__(self, seg1=None, seg2=None, seg1_ind=None,\
            seg2_ind=None, coordinate=None, list_segs=None):
        if coordinate is not None:
            self.coordinate = coordinate
            self.segments = list_segs
        else:
            self.coordinate = intersection(seg1, seg2)
            self.segments = [seg1_ind, seg2_ind]
        control.plot_disc(self.coordinate[0], self.coordinate[1],\
                            "yellow", 6.0)

def pre_process (segments_in):
    fix_segments(segments_in)
    keys = [0 for i in range (len(segments_in))]
    seg_map = {}
    segments_out = sorted(segments_in,\
                key=functools.cmp_to_key(compare_segments))
    heap, hmap = make_event_points(segments_out)
    for i in range (len(segments_out)):
        keys[i] = segments_out[i].init
        seg_map[segments_out[i]] = i
    return segments_out, keys, heap, hmap, seg_map
def base_draw (segments):
    for s in segments:
        s.plot()

def get_initial_intersection (event_pt, evt_hmap, evt_heap, list_inter):
    segs_inter = set().union(event_pt.left, event_pt.right,\
                             event_pt.intersections)
    if len(segs_inter) == 1: return
    inter = intersection_locator(coordinate=event_pt.get_coordinate(),\
                             list_segs=segs_inter)
    for seg in inter.segments:
        event_pt.add_to_segment(seg, -1)
    list_inter.append(inter)

def update_sweepline (bst, evt_pt, list_seg, list_keys, evt_heap,\
                       evt_hmap, seg_map, list_inter):
    #End of an exhisting segment
    for seg_ind in evt_pt.right:
        intersected, intersections = treat_right(seg_ind, list_seg, list_keys, seg_map, bst)
        if(intersected):
            for inter in intersections:
                make_event(evt_hmap, evt_heap, inter.segments, inter.coordinate, -1)
                list_inter.append(inter)
    #Intersections on the point (no specific order)
    intersected, intersections = treat_intersection(evt_pt.get_coordinate(), evt_pt.intersections, list_seg, list_keys, seg_map, bst)
    if(intersected):
        for inter in intersections:
            make_event(evt_hmap, evt_heap, inter.segments, inter.coordinate, -1)
            list_inter.append(inter)
    # Start of a new segment
    for seg_ind in evt_pt.left:
        intersected, intersections = treat_left(seg_ind, list_seg, list_keys, seg_map, bst)
        if(intersected):
            for inter in intersections:
                make_event(evt_hmap, evt_heap, inter.segments, inter.coordinate, -1)
                list_inter.append(inter)
    for seg_ind in evt_pt.intersections:
        bst.insert(list_keys[seg_ind], list_seg[seg_ind])

# Scanline algorithm to find all intersections between segments
#  in a plane
def Scanline (segments):
    segments, seg_keys, heap, hmap, seg_map = pre_process(segments)
    intersections = []
    bst = RBTree()
    base_draw(segments)
    while (not heap.empty()):
        pt = heap.get()
        circ = control.plot_circle(pt.node.x, pt.node.y, "green", 2)
        control.sleep()
        get_initial_intersection(pt, hmap, heap, intersections)
        update_sweepline (bst, pt, segments, seg_keys, heap, hmap,\
                          seg_map, intersections)
        control.plot_delete(circ)
    print (bst._count)
    print_aux2(intersections)
    return intersections

# auxiliary prints
def print_aux2(list_intersections):
    for inter in list_intersections:
        print("\n\n============")
        print("point = ", inter.coordinate)
        for seg in inter.segments:
            print("segment = ", seg)

def print_aux1(pt, segs):
    print(pt.node.x, pt.node.y)
    print("Ponto extremo dos segmentos:")
    for seg in pt.segments:
        print(segs[seg[0]])
    print("Ponto de interseccao entre os segmentos:")
    for inter in pt.intersections:
        print(inter[0], inter[1])