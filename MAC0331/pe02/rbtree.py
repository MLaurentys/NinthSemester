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

from .abctree import ABCTree
from geocomp.lineintersections.segments_math import at_left
__all__ = ['RBTree']


class RBNode(object):
    """Internal object, represents a tree node."""
    __slots__ = ['key', 'value', 'red', 'left', 'right']

    def __init__(self, key=None, value=None):
        self.key = key #reference point
        self.value = value #segment
        self.red = True
        self.left = None
        self.right = None

    def free(self):
        self.left = None
        self.right = None
        self.key = None
        self.value = None

    def __getitem__(self, key):
        """N.__getitem__(key) <==> x[key], where key is 0 (left) or 1 (right)."""
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """N.__setitem__(key, value) <==> x[key]=value, where key is 0 (left) or 1 (right)."""
        if key == 0:
            self.left = value
        else:
            self.right = value

    def __lt__(self, other):
        if self.value.has_left(other.key):return True
        if other.value.has_left(self.key):return False
        if self.value.has_left(other.value.to): return True
        return False

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

    def _new_node(self, key, value):
        """Create a new tree node."""
        self._count += 1
        return RBNode(key, value)

    def get_value(self, key):
        node = self._root
        while node is not None:
            if node.value.has_left(key):
                node = node.right
            elif node.value.colinear_with(key):
                return node.value
            else:
                node = node.left
        return None

    def succ_item(self, key):
        node = self._root
        succ_node = None
        while node is not None:
            if key == node.key:
                break
            elif node.value.has_left(key):
                node = node.right
            else:
                if (succ_node is None) or node.value.has_left(succ_node.key):
                    succ_node = node
                node = node.left
        if node is None:  # stay at dead end
            #raise KeyError(str(key))
            return None, None
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
            #raise KeyError(str(key))
            return None, None
        return succ_node.key, succ_node.value

    def prev_item(self, key):
        """Get predecessor (k,v) pair of key, raises KeyError if key is min key
        or key does not exist. optimized for pypy.
        """
        # removed graingets version, because it was little slower on CPython and much slower on pypy
        # this version runs about 4x faster with pypy than the Cython version
        # Note: Code sharing of prev_item() and floor_item() is possible, but has always a speed penalty.
        node = self._root
        prev_node = None

        while node is not None:
            if key == node.key:
                break
            elif node.value.has_left(key):
                node = node.left
            else:
                if (prev_node is None) or prev_node.value.has_left(node.key):
                    prev_node = node
                node = node.right

        if node is None:  # stay at dead end (None)
            #raise KeyError(str(key))
            return None, None
        # found node of key
        if node.left is not None:
            # find biggest node of left subtree
            node = node.left
            while node.right is not None:
                node = node.right
            if prev_node is None:
                prev_node = node
            elif node > prev_node:
                prev_node = node
        elif prev_node is None:  # given key is smallest in tree
            #raise KeyError(str(key))
            return None, None
        return prev_node.key, prev_node.value

    def get_neighbours (self, key):
        return self.prev_item(key), self.succ_item(key)

    def insert(self, key, value):
        """T.insert(key, value) <==> T[key] = value, insert key, value into tree."""
        if self._root is None:  # Empty tree case
            self._root = self._new_node(key, value)
            self._root.red = False  # make root black
            return

        head = RBNode()  # False tree root
        grand_parent = None
        grand_grand_parent = head
        parent = None  # parent
        direction = 0
        last = 0

        # Set up helpers
        grand_grand_parent.right = self._root
        node = grand_grand_parent.right
        # Search down the tree
        while True:
            if node is None:  # Insert new node at the bottom
                node = self._new_node(key, value)
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
            if key == node.key:
                node.value = value  # set new value for key
                break

            last = direction
            direction = 0 if node.value.has_left(key) else 1 #key < node.key
            # Update helpers
            if grand_parent is not None:
                grand_grand_parent = grand_parent
            grand_parent = parent
            parent = node
            node = node[direction]

        self._root = head.right  # Update root
        self._root.red = False  # make root black

    def remove(self, key):
        """T.remove(key) <==> del T[key], remove item <key> from tree."""
        if self._root is None:
            raise KeyError(str(key))
        head = RBNode()  # False tree root
        node = head
        node.right = self._root
        parent = None
        grand_parent = None
        found = None  # Found item
        direction = 1

        # Search and push a red down
        while node[direction] is not None:
            last = direction

            # Update helpers
            grand_parent = parent
            parent = node
            node = node[direction]

            #direction = 1 if key > node.key else 0
            direction = 0 if node.value.has_left(key) else 1

            # Save found node
            if key == node.key:
                found = node

            # Push the red node down
            if not is_red(node) and not is_red(node[direction]):
                if is_red(node[1 - direction]):
                    parent[last] = jsw_single(node, direction)
                    parent = parent[last]
                elif not is_red(node[1 - direction]):
                    sibling = parent[1 - last]
                    if sibling is not None:
                        if (not is_red(sibling[1 - last])) and (not is_red(sibling[last])):
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
            found.key = node.key
            found.value = node.value
            parent[int(parent.right is node)] = node[int(node.left is None)]
            node.free()
            self._count -= 1

        # Update root and make it black
        self._root = head.right
        if self._root is not None:
            self._root.red = False
        if not found:
            raise KeyError(str(key))
