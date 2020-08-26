"""Sweepline algorithm for line intersections"""
import queue
import functools
from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config
from geocomp import colors
from .node_types import *
from .abb import sweep_bst
from .additional_math import *

##############################
###
### PE 2 - START
###
##############################

event_heap = queue.PriorityQueue()
event_pt_map = {} # Point -> Node_Event
bst = sweep_bst()

#
# Makes the points the scanline is going to stop at
#

def make_event (segment, point, position):
    global event_heap, event_pt_map
    #position 0: left
    #position 1: right
    #position -1: intersection -> segment = [seg1, seg2]
    pt = (point[0], point[1])
    if pt in event_pt_map:
        node_event = event_pt_map[pt]
        node_event.add_to_segment(segment, position)
    else:
        new_event = Node_Event(pt)
        new_event.add_to_segment(segment, position)
        event_heap.put(new_event)
        event_pt_map[pt] = new_event

# Makes initial map and queue of the segments limits
def make_event_points (segs):
    global event_heap, event_pt_map
    event_heap = queue.PriorityQueue()
    event_pt_map = {}
    for seg in segs:
        make_event (seg, seg.init, 0)
        make_event (seg, seg.to, 1)

##
## Sweep-line
##

# Called once for every event, will print the segments that intersect
def print_intersection(event):
    if len(event.left) + len(event.right) + len(event.intersections) > 1:
        print("Intersection at (%f, %f)\nSegments:"
              % (event.node.x, event.node.y))
        event.node.get_point().hilight(color="yellow")
        for seg in event.left.union(event.right).union(event.intersections):
            print(seg)

# Finds the collisions resultant of the last event
def find_collision(event):
    global bst, event_pt_map
    pred = bst.predecessor(event.node.get_point())
    succ = bst.sucessor(event.node.get_point())
    for segs in [pred, succ]:
        if segs[0] is None or segs[1] is None:
            continue
        segs[0].hilight("blue")
        segs[1].hilight("blue")
        control.sleep()
        if segs[0].intersects(segs[1]):
            inter_pt = intersection(segs[0], segs[1])
            make_event(segs, inter_pt, -1)
        segs[0].unhilight()
        segs[1].unhilight()
    # Lida com caso..

# Called once for each event, updates to bst to reflect the state of the
#  sweep-line on top of the event
def update_bst(event):
    global bst
    pt = event.node.get_point()
    int_r = event.right.union(event.intersections)
    for seg in event.right:
        bst.remove(seg, pt)
        int_r.remove(seg)
        seg.hilight("#ff8888")
    inters = list(int_r)
    for seg in inters:
        bst.remove(seg, pt)
    for seg in inters:
        bst.insert(seg, pt)
    for seg in event.left:
        seg.hilight("#8888ff")
        bst.insert(seg, pt)

# Makes segment.start <= segment.end
def fix_segments (l):
    l = list(set(l))
    for i in range (len(l)):
        res = compare_points(l[i].init, l[i].to)
        if (res > 0):
            l[i].init, l[i].to = l[i].to, l[i].init
    for i in range (len(l)):
        l[i].plot()

# Scanline algorithm to find all intersections between segments in a plane
def sweepline (segments):
    global event_heap, bst
    fix_segments(segments)
    bst = sweep_bst()
    segments = sorted(segments, key=functools.cmp_to_key(compare_segments))
    #testa_bst(bst, segments)
    make_event_points(segments)
    while (not event_heap.empty()):
        pt = event_heap.get()
        circ = control.plot_circle(pt.node.x, pt.node.y, "green", 2)
        control.sleep()
        if len(pt.intersections) + len(pt.right) == 0:
            seg = bst.search(pt.node.get_point())
            if seg is not None:  # um único segmento na árvore contem pt
                                 #  e pt é extremo esquerdo de alguns segmentos
                pt.add_to_segment([seg], -1)
        update_bst(pt)
        find_collision(pt)
        print_intersection(pt)
        control.plot_delete(circ)