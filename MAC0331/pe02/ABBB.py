from geocomp.lineintersections.node_types import Node_Seg

# BST data structure that should work for any comparable (class that implements __lt__)
class ABBB:
    def __init__(self, node_ctor=None):
        super().__init__()
        self._root = None
        self._Node = node_ctor

    def get (self, val):
        nd = self._Node(val)
        if (self._root == None):
            return None
        node = self._root
        while (node is not None):
            if (nd < node):
                node = node.left
            elif node < nd:
                node = node.right
            else:
                break
        return node

    def _insert (self, nd):
        if (self._root == None):
            self._root = nd
            return
        node = self._root
        par = None
        while (node is not None):
            par = node
            if (nd < node):
                node = node.left
            else:
                node = node.right
        if (nd < par):
            par.left = nd
        else:
            par.right = nd

    def insert(self, val):
        if (type(val) == Node_Seg): #very ugly line i cannot replace?
            self._insert(val)
        else:
            nd = self._Node(val)
            self._insert(nd)


    def _remove(self, cur_node, node):
        if (cur_node is None):
            print ("ERROOOOO NAO REMOVEU!!!!!!!!!!!")
            return None
        if (node < cur_node):
            cur_node.left = self._remove(cur_node.left, node)
        elif (cur_node < node):
            cur_node.right = self._remove(cur_node.right, node)
        else:
            if (cur_node.left is None):
                ret = cur_node.right
                cur_node.left = None
                cur_node.right = None
                return ret
            elif (cur_node.right is None):
                ret = cur_node.left
                cur_node.left = None
                cur_node.right = None
                return ret
            else:
                n_node = self.get_min(cur_node.right)
                st, en, k, sg = n_node.get_val()
                cur_node.set_val(st, en, k, sg)
                cur_node.right = self._remove(cur_node.right, n_node)
                n_node.left = None
                n_node.right = None
        return cur_node


    def remove(self, val):
        if (type(val) == Node_Seg):
            self._root = self._remove(self._root, val)
        else:
            nd = self._Node(val)
            nd.change_key(nd.end.get_point())
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

    def print_tree(self):
        print("===== TREE =========\n")
        if self._root is not None:
            self._print_tree(self._root)
        print("===== END =========\n")

    def _print_tree(self, tree_node):
        if tree_node.left is not None:
            self._print_tree(tree_node.left)
        print(tree_node.seg)
        if tree_node.right is not None:
            self._print_tree(tree_node.right)

    def _get_neighbour(self, start, node):
        if start == None: return None, None
        pred = succ = None
        if start < node:
            pred = start
            a_pred, a_succ = self._get_neighbour(start.right, node)
            if a_pred is not None and pred < a_pred: pred = a_pred
            succ = a_succ
        elif node < start:
            succ = start
            a_pred, a_succ = self._get_neighbour(start.right, node)
            if a_succ is not None and a_succ < succ: succ = a_succ
            pred = a_pred
        else:
            if start.left is not None:
                t = start.left
                while t.right is not None:
                    t = t.right
                pred = t
            if start.right is not None:
                t = start.right
                while t.left is not None:
                    t = t.left
                succ = t
        return pred, succ

    def get_neighbours(self, val):
        if type(val) == Node_Seg:
            ns = self._get_neighbour(self._root, val)
        else:
            nd = self._Node(val)
            ns = self._get_neighbour(self._root, nd)
        ns1 = ns[0].seg if ns[0] is not None else None
        ns2 = ns[1].seg if ns[1] is not None else None
        return ns1, ns2
