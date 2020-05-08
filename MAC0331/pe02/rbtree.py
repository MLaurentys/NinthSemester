#!/usr/bin/env python
# coding:utf-8
# Author:  mozman (python version)
# Purpose: red-black tree module (Julienne Walker's none recursive algorithm)
# source: http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_rbtree.aspx
# Created: 01.05.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

# Conclusion of Julian Walker

# Red black trees are interesting beasts. They're believed to be simpler than
# AVL trees (their direct competitor), and at first glance this seems to be the
# case because insertion is a breeze. However, when one begins to play with the
# deletion algorithm, red black trees become very tricky. However, the
# counterweight to this added complexity is that both insertion and deletion
# can be implemented using a single pass, top-down algorithm. Such is not the
# case with AVL trees, where only the insertion algorithm can be written top-down.
# Deletion from an AVL tree requires a bottom-up algorithm.

# So when do you use a red black tree? That's really your decision, but I've
# found that red black trees are best suited to largely random data that has
# occasional degenerate runs, and searches have no locality of reference. This
# takes full advantage of the minimal work that red black trees perform to
# maintain balance compared to AVL trees and still allows for speedy searches.

# Red black trees are popular, as most data structures with a whimsical name.
# For example, in Java and C++, the library map structures are typically
# implemented with a red black tree. Red black trees are also comparable in
# speed to AVL trees. While the balance is not quite as good, the work it takes
# to maintain balance is usually better in a red black tree. There are a few
# misconceptions floating around, but for the most part the hype about red black
# trees is accurate.

from __future__ import absolute_import

from geocomp.lineintersections.abctree import ABCTree

__all__ = ['RBTree']

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

class RBNode (object):
    """Internal object, represents a tree node."""
    __slots__ = ['seg', 'start', 'end', 'red', 'past_middle', 'key', 'left', 'right']

    def __init__(self, seg):
        if seg is None:
            self.seg = None
            self.start = None
            self.end = None
        else:
            self.seg = seg
            self.start = Node(seg.init)
            self.end = Node(seg.to)
        self.red = True
        self.past_middle = False
        self.key = self.start
        self.left = None
        self.right = None

    def set_key(self, node) :
        self.key = node

    def free(self):
        self.left = None
        self.right = None
        self.key = None
        self.seg = None
        self.start = None
        self.end = None
    def __getitem__(self, pos):
        """x[pos], where pos is 0 (left) or 1 (right)."""
        return self.left if pos == 0 else self.right

    def __setitem__(self, pos, node):
        """x[pos]=value, where pos is 0 (left) or 1 (right)."""
        if pos == 0:
            self.left = node
        elif pos == 1:
            self.right = node
            
    def get_val(self):
        return self.start, self.end, self.past_middle, self.seg

    def mark(self):
        self.mark = True

    def set_val(self, start, end, pm, seg):
        self.start = start
        self.end = end
        self.past_middle = pm
        self.seg = seg

    def __lt__(self, other):
        s_comp_1 = self.start
        s_comp_2 = self.end
        o_comp_1 = other.start
        o_comp_2 = other.end
        if self.mark:
            s_comp_1 = self.end
            s_comp_2 = self.start
        if other.mark:
            o_comp_1 = other.end
            o_comp_2 = other.start

        if s_comp_1.y < o_comp_1.y:
            return True
        else:
            if (o_comp_1.y < s_comp_1.y):
                return False
            else:
                return s_comp_2.y < o_comp_2.y


def is_red(node):
    if (node is not None) and node.red:
        return True
    else:
        return False


def jsw_single(root, direction):
    other_side = 1 - direction
    save = root[other_side]
    root[other_side] = save[direction]
    save[direction] = root
    root.red = True
    save.red = False
    return save


def jsw_double(root, direction):
    other_side = 1 - direction
    root[other_side] = jsw_single(root[other_side], other_side)
    return jsw_single(root, direction)


class RBTree(ABCTree):
    """
    RBTree implements a balanced binary tree with a dict-like interface.

    see: http://en.wikipedia.org/wiki/Red_black_tree

    A red-black tree is a type of self-balancing binary search tree, a data
    structure used in computing science, typically used to implement associative
    arrays. The original structure was invented in 1972 by Rudolf Bayer, who
    called them "symmetric binary B-trees", but acquired its modern name in a
    paper in 1978 by Leonidas J. Guibas and Robert Sedgewick. It is complex,
    but has good worst-case running time for its operations and is efficient in
    practice: it can search, insert, and delete in O(log n) time, where n is
    total number of elements in the tree. Put very simply, a red-black tree is a
    binary search tree which inserts and removes intelligently, to ensure the
    tree is reasonably balanced.

    RBTree() -> new empty tree.
    RBTree(mapping) -> new tree initialized from a mapping
    RBTree(seq) -> new tree initialized from seq [(k1, v1), (k2, v2), ... (kn, vn)]

    see also abctree.ABCTree() class.
    """

    def _new_node(self, seg):
        """Create a new tree node."""
        self._count += 1
        return RBNode(seg)

    def insert(self, seg):
        if self._root is None:  # Empty tree case
            self._root = self._new_node(seg)
            self._root.red = False  # make root black
            return

        head = RBNode(None)  # False tree root
        grand_parent = None
        grand_grand_parent = head
        parent = None  # parent
        direction = 0
        last = 0
        new_node = RBNode(seg)
        # Set up helpers
        grand_grand_parent.right = self._root
        node = grand_grand_parent.right
        # Search down the tree
        while True:
            if node is None:  # Insert new node at the bottom
                node = self._new_node(seg)
                parent[direction] = node
            elif is_red(node.left) and is_red(node.right):  # Color flip
                node.red = True
                node.left.red = False
                node.right.red = False

            # Fix red violation
            if is_red(node) and is_red(parent):
                direction2 = 1 if grand_grand_parent.right is grand_parent else 0
                if node is parent[last]:
                    grand_grand_parent[direction2] = jsw_single(grand_parent, 1 - last)
                else:
                    grand_grand_parent[direction2] = jsw_double(grand_parent, 1 - last)

            # Stop if found
            #if not (new_node < node or node < new_node) :

            last = direction
            if new_node < node :
                direction = 0
            elif node < new_node :
                direction = 1
            else :
                st, en, pm, sg = new_node.get_val()
                node.set_val(st, en, pm, sg)
                break

            # Update helpers
            if grand_parent is not None:
                grand_grand_parent = grand_parent
            grand_parent = parent
            parent = node
            node = node[direction]

        self._root = head.right  # Update root
        self._root.red = False  # make root black

    def remove(self, seg):
        """T.remove(key) <==> del T[key], remove item <key> from tree."""
        if self._root is None:
            raise KeyError(str(seg))
        head = RBNode(None)  # False tree root
        node = head
        node.right = self._root
        parent = None
        grand_parent = None
        found = None  # Found item
        direction = 1
        node_to_remove = RBNode(seg)
        # Search and push a red down
        while node[direction] is not None:
            last = direction

            # Update helpers
            grand_parent = parent
            parent = node
            node = node[direction]

            if node_to_remove < node :
                direction = 0
            elif node < node_to_remove :
                direction = 1
            else :
                found = node

            # Push the red node down
            if not is_red(node) and not is_red(node[direction]):
                if is_red(node[1 - direction]):
                    parent[last] = jsw_single(node, direction)
                    parent = parent[last]
                elif not is_red(node[1 - direction]):
                    sibling = parent[1 - last]
                    if sibling is not None:
                        if (not is_red(sibling[1 - last])) \
                            and (not is_red(sibling[last])):
                            # Color flip
                            parent.red = False
                            sibling.red = True
                            node.red = True
                        else:
                            direction2 = 1 if grand_parent.right is parent else 0
                            if is_red(sibling[last]):
                                grand_parent[direction2] = jsw_double(parent, last)
                            elif is_red(sibling[1 - last]):
                                grand_parent[direction2] = jsw_single(parent, last)
                            # Ensure correct coloring
                            grand_parent[direction2].red = True
                            node.red = True
                            grand_parent[direction2].left.red = False
                            grand_parent[direction2].right.red = False

        # Replace and remove if found
        if found is not None:
            st, en, pm, sg = node.get_val()
            found.set_val(st, en, pm, sg)
            parent[int(parent.right is node)] = node[int(node.left is None)]
            node.free()
            self._count -= 1

        # Update root and make it black
        self._root = head.right
        if self._root is not None:
            self._root.red = False
        if not found:
            raise KeyError(str(seg))

    def _prev_item(self, target):
        node = self._root
        prev_node = None

        while node is not None:
            if target < node:
                node = node.left
            elif (prev_node is None) or (prev_node < node):
                prev_node = node
                node = node.right
            else:
                break

        if node is None:  # stay at dead end (None)
            return None
        # found node of key
        if node.left is not None:
            # find biggest node of left subtree
            node = node.left
            while node.right is not None:
                node = node.right
            if prev_node is None:
                prev_node = node
            elif prev_node > node:
                prev_node = node
        elif prev_node is None:  # given key is smallest in tree
            prev_node = None
        return prev_node
    def _succ_item(self, target):
        node = self._root
        succ_node = None
        while node is not None:
            if target < node:
                if (succ_node is None) or (node.key < succ_node.key):
                    succ_node = node
                node = node.left
            elif node < target:
                node = node.right
            else:
                break
        if node is None:  # stay at dead end
            return None
        # found node of key
        if node.right is not None:
            # find smallest node of right subtree
            node = node.right
            while node.left is not None:
                node = node.left
            if succ_node is None:
                succ_node = node
            elif node < succ_node:
                succ_node = node
        elif succ_node is None:  # given key is biggest in tree
            succ_node = None
        return succ_node

    def get_neighbours(self, seg):
        node = RBNode(seg)
        prev = self._prev_item(node)
        succ = self._succ_item(node)
        p = s = None
        if prev is not None: p = prev.seg 
        if succ is not None: s = succ.seg 
        return p, s 