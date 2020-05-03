# BST data structure that should work for any comparable (class that implements __lt__)
class ABBB:
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

    def cheat_insert(self, val, compare):
        nd = self._Node(val)
        if (self._root == None):
            self._root = nd
            return
        node = self._root
        par = None
        while (node):
            par = node
            if (compare(nd, node)):
                node = node.left
            else:
                node = node.right
        if (compare(nd, par)):
            par.left = nd
        else:
            par.right = nd

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
                cur_node = None
                return ret
            elif (cur_node.right is None):
                ret = cur_node.left
                cur_node = None
                return ret
            else:
                n_node = self.get_min(cur_node.right)
                s,e = n_node.get_val()
                cur_node.set_val(s,e)
                cur_node.right = self._remove(cur_node.right, n_node)
        return cur_node


    def remove(self, val):
        nd = self._Node(val)
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

    def _get_neighbour(self, node):
        def find_left(start, node):
                ret = None
                if(start != None):
                    if (start < node):
                        temp = find_left(start.right, node)
                        ret = temp if (temp) else start
                    else:
                        ret = find_left(start.left, node)
                return ret
        def find_right(start, node):
            ret = None
            if(start != None):
                if (node < start):
                    temp = find_right(start.left, node)
                    ret = temp if(temp) else start
                else:
                    ret = find_right(start.right, node)
            return ret
        
        return find_left(self._root, node), find_right(self._root, node)

    def get_neighbours(self, val):
        nd = self._Node(val)
        ns = self._get_neighbour(nd)
        ns1 = ns[0].seg if(ns[0]) else None
        ns2 = ns[1].seg if(ns[1]) else None
        return ns1, ns2
