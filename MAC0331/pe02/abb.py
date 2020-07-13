from geocomp.common.prim import left, collinear, right
from .node_types import Node_Seg as Node

class sweep_bst:

    def __init__ (self):
        self._root = None
        self._size = 0

    def insert (self, seg, reference):
        if self._root is None:
            self._root = Node(seg)
        else:
            self._insert(self._root, seg, reference)
        self._size += 1

    def remove (self, seg, reference):
        self._root = self._remove(self._root, seg, reference)
        self._size -= 1
 
    def predecessor (self, reference):
        return self._predecessor(self._root, reference, None, None)

    def sucessor (self, reference):
        return self._sucessor(self._root, reference, None, None)

    def _remove (self, node, seg, reference):
        if node is None:
            raise Exception("Removing item not present on bst")
        if seg == node.seg:
            if (node.left is None):
                ret = node.right
                node = None
                return ret
            elif (node.right is None):
                ret = node.left
                node = None
                return ret
            else:
                n_node = self.get_min(node.right)
                n_node_seg = n_node.get_val()
                node.set_val(n_node_seg)
                node.right = self._remove(node.right, n_node_seg, reference)
        elif self._del_comp(node.seg, seg, reference):
            node.left = self._remove(node.left, seg, reference)
        else:
            node.right = self._remove(node.right, seg, reference)
        return node

    # returns minimum node available starting at node
    def get_min(self, node):
        par = node
        while par.left is not None:
            par = par.left
        return par

    def _insert (self, node, seg, reference):
        if self._ins_comp(node.seg, seg, reference):
            if node.left is None:
                node.left = Node(seg)
            else:
                self._insert(node.left, seg, reference)
        else:
            if node.right is None:
                node.right = Node(seg)
            else:
                self._insert(node.right, seg, reference)

    def _ins_comp (self, seg1, seg2, reference):
        return left(seg1.init, seg1.to, reference) or\
               (collinear(seg1.init, seg1.to, reference) and #if ties
                left(seg1.init, seg1.to, seg2.to)) # looks at endpoint

    def _del_comp (self, seg1, seg2, reference):
        return left(seg1.init, seg1.to, reference) or\
               (collinear(seg1.init, seg1.to, reference) and #if ties
                left(seg1.init, seg1.to, seg2.init)) # looks at starting point

    def _pred_comp (self, seg, reference):
        return left(seg.init, seg.to, reference) or\
               collinear(seg.init, seg.to, reference)

    def _succ_comp(self, seg, reference):
        return right(seg.init, seg.to, reference) or\
               collinear(seg.init, seg.to, reference)

    def _predecessor (self, node, reference, pred_seg, prim_seg):
        if node is None:
            return (pred_seg, prim_seg)
        if self._pred_comp(node.seg, reference):
            return self._predecessor(node.left, reference, pred_seg, node.seg)
        return self._predecessor(node.right, reference, node.seg, prim_seg)

    def _sucessor (self, node, reference, last_seg, succ_seg):
        if node is None:
            return (last_seg, succ_seg)
        if self._succ_comp(node.seg, reference):
            return self._sucessor(node.right, reference, node.seg, succ_seg)
        return self._sucessor(node.left, reference, last_seg, node.seg)
