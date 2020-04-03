#!/usr/bin/env python
"""Scanline algorithm for line intersections"""
import queue
import functools
from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config

class Node:
    def __init__(self, pt):
        super().__init__()
        self.left = None
        self.right = None
        self.x = pt.x
        self.y = pt.y

    def __lt__(self, other):
        if (self.x == other.x):
            return self.y < other.y
        else:
            return self.x < other.x


class ABB:
    def __init__(self):
        super().__init__()
        self._root = None
    
    def insert(self, point):
        nd = Node(point.init, point.to)
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

    def remove(self, point):
        nd = Node(point.init, point.to)
        if (self._root == None):
            return False, None
        node = self._root
        par = None
        while (node):
            par = node
            if (nd < node):
                node = node.left
            elif (node < nd):
                node = node.right
            else:
                
                return True
        if (nd < par):
            par.left = nd
        else:
            par.right = nd

    def remove_min(self, node):
        par = None
        while (node):
            par = node
            if (node.left):
                node = node.left
            else:
                pass

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

def make_event_points (segments):
    heap = queue.PriorityQueue()
    for s in segments:
        heap.put(Node(s.init))
        heap.put(Node(s.to))
    return heap



def Scanline (segments):
    fix_segments(segments)
    segments = sorted(segments, key=functools.cmp_to_key(compare_segments))
    heap = make_event_points(segments)

    for i in range (len(segments)):
        print(str(i) +": " + str(segments[i]))
        segments[i].plot()
    
    while (not heap.empty()):
        pt = heap.get() 