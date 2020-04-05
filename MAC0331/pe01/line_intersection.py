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

class Node_Seg:
    def __init__(self, seg):
        super().__init__()
        self.left = None
        self.right = None
        self.start = Node(seg.init)
        self.end = Node(seg.to)

    def get_val(self):
        return self.start, self.end

    def set_val(self, start, end):
        self.start = start
        self.end = end

    def __lt__(self, other):
        return self.start < other.start

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
            cur_node.left = _remove(cur_node.left, node)
        elif (cur_node < node):
            cur_node.right = _remove(cur_node.right, node)
        else:
            if (cur_node.left is None):
                ret = cur_node.right
                cur_node = None
            elif (cur_node.right is None):
                ret = cur_node.left
                cur_node = None
            else:
                n_node = get_min(cur_node.right)
                cur_node.set_val(n_node.get_val())
                _remove(cur_node.right, n_node)
                ret = cur_node
            cur_node = ret
        return cur_node


    def remove(self, val):
        nd = self._Node(val)
        return _remove(self._root, Node)

    def get_min(self, node):
        par = None
        nd = node
        while (nd):
            par = nd
            nd = nd.left
        return par




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