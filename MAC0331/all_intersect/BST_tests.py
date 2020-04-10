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

class Node_Seg:
    def __init__(self, seg):
        super().__init__()
        self.left = None
        self.right = None
        self.seg = seg
        self.start = Node(seg[0])
        self.end = Node(seg[1])

    def get_val(self):
        return self.start, self.end

    def set_val(self, start, end):
        self.start = start
        self.end = end

    def __lt__(self, other):
        if self.start < other.start:
            return True
        else:
            if (other.start < self.start):
                return False
            else:
                return self.end < other.end

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

bst = ABB(Node_Seg)
a = [[ ( 57.0, 17.0 ), ( git add96.0, 5.0 ) ], [ ( 49.0, 40.0 ), ( 60.0, 61.0 ) ], [ ( 2.0, 36.0 ), ( 36.0, 90.0 ) ], [ ( 2.0, 36.0 ), ( 17.0, 28.0 ) ], [ ( 50.0, 32.0 ), ( 79.0, 71.0 ) ], [ ( 51.0, 87.0 ), ( 92.0, 46.0 ) ], [ ( 22.0, 11.0 ), ( 34.0, 41.0 ) ], [ ( 47.0, 44.0 ), ( 65.0, 57.0 ) ], [ ( 15.0, 25.0 ), ( 41.0, 4.0 ) ], [ ( 83.0, 15.0 ), ( 93.0, 15.0 ) ], [ ( 75.0, 89.0 ), ( 83.0, 25.0 ) ]]
b = [[ ( 2.0, 36.0 ), ( 17.0, 28.0 ) ], [ ( 2.0, 36.0 ), ( 36.0, 90.0 ) ], [ ( 15.0, 25.0 ), ( 41.0, 4.0 ) ], [ ( 22.0, 11.0 ), ( 34.0, 41.0 ) ], [ ( 47.0, 44.0 ), ( 65.0, 57.0 ) ], [ ( 49.0, 40.0 ), ( 60.0, 61.0 ) ], [ ( 50.0, 32.0 ), ( 79.0, 71.0 ) ], [ ( 51.0, 87.0 ), ( 92.0, 46.0 ) ], [ ( 57.0, 17.0 ), ( 96.0, 5.0 ) ], [ ( 75.0, 89.0 ), ( 83.0, 25.0 ) ], [ ( 83.0, 15.0 ), ( 93.0, 15.0 ) ]]

print("======================\n      INSERTING\n======================")
for seg in a:
    print(seg)
    bst.insert(seg)
print("======================\n      NEIGHBORS\n======================")
for i in range (1, len(b) - 1):
    segs = bst.get_neighbours(b[i])
    print(segs[0], b[i], segs[1])
    print(segs[0] == b[i-1])
    print(segs[1] == b[i+1])
print("======================\n      REMOVING\n======================")
print(bst.is_empty())
for seg in a:
    print(seg)
    n = bst.remove(seg)

print(bst.is_empty())