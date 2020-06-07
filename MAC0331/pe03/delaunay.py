from random import shuffle
import networkx as nx
import matplotlib.pyplot as plt
from geocomp.common.point import Point
from geocomp.common.segment import Segment
from geocomp.common.prim import left, collinear, on_segment
from geocomp.common import control
from geocomp.triangulation.triangle_node import Node
from geocomp.triangulation.DCEL import hedge, DCEL

root = None
DG = None
dcel = None


def pre_process (points):
    global DG, dcel, root
    shuffle(points)
    inside = []
    not_inside = [i for i in range(len(points))]
    min_x = min_y = float('inf')
    max_x = max_y = -float('inf')
    for i, pt in enumerate(points):
        if pt.x < min_x: min_x = pt.x
        if pt.x > max_x: max_x = pt.x
        if pt.y > max_y: max_y = pt.y
        if pt.y < min_y: min_y = pt.y
        points[i] = Point(pt[0], pt[1])
    mid_hor = (max_x + min_x) / 2.0  #fixed
    left_hor = mid_hor - (max_x - min_x) * 0.75 #fixed
    hor_fact = (max_x - min_x) #variable
    mid_ver = (max_y + min_y) / 2.0  #fixed
    len_ver = (max_y - min_y)        #variable
    node = None
    while (len(not_inside) > 0):
        node = Node(Point(left_hor, mid_ver + len_ver), #top left
                    Point(left_hor, mid_ver - len_ver), #bottom left
                    Point(mid_hor + hor_fact, mid_ver)) #center right
        for i in range(len(not_inside)):
            if node.contains_proper(points[not_inside[i]]):
                inside.append(i)
        for ind in reversed(inside):
            not_inside.pop(ind)
        inside = []
        hor_fact *= 1.15
        len_ver *= 1.5
    DG = nx.DiGraph()
    dcel = DCEL()
    root = node
    DG.add_node(root)
    vtcs = root.get_vertices()

    ext1 = hedge(vtcs[1], vtcs[0])
    ext2 = hedge(vtcs[0], vtcs[2])
    ext3 = hedge(vtcs[2], vtcs[1])
    int1 = hedge(vtcs[0], vtcs[1])
    int2 = hedge(vtcs[2], vtcs[0])
    int3 = hedge(vtcs[1], vtcs[2])

    ext1.next = ext2
    ext1.prev = ext3
    ext1.twin = int1
    ext2.next = ext3
    ext2.prev = ext1
    ext2.twin = int2
    ext3.next = ext1
    ext3.prev = ext2
    ext3.twin = int3

    int1.next = int3
    int1.prev = int2
    int1.twin = ext1
    int1.face = root
    int2.next = int1
    int2.prev = int3
    int2.twin = ext2
    int2.face = root
    int3.next = int2
    int3.prev = int1
    int3.twin = ext3
    int3.face = root

    dcel.add_hedge(ext1)
    dcel.add_hedge(ext2)
    dcel.add_hedge(ext3)
    dcel.add_hedge(int1)
    dcel.add_hedge(int2)
    dcel.add_hedge(int3)

def post_process():
    global root, DG, dcel
    verts = root.get_vertices()
    he1 = dcel.get_hedge((root.v2, root.v1))
    he2 = dcel.get_hedge((root.v3, root.v2))
    he3 = dcel.get_hedge((root.v1, root.v3))
    to_remove = set([he1, he2, he3]) #set of hedges in external face
    to_fix = set() # faces that needs fixing
    while (len(to_remove) > 0):
        he = to_remove.pop()
        if he not in dcel.hedges.values():
            continue # twin was already fixed
        twin = dcel.get_twin(he)
        if he.origin not in verts and he.destine not in verts:
            to_fix.add(twin.face)
            continue
        he.prev.next = twin.next
        twin.next.prev = he.prev
        he.next.prev = twin.prev
        twin.prev.next = he.next

        twin.prev.face = None
        twin.next.face = None

        dcel.remove_edge(he.origin, he.destine, True)

        to_remove.add(twin.next)
        to_remove.add(twin.prev)

    fix_illegal(to_fix)



def add_to_normal_case (par, pt):
    global DG, dcel
    # adds three new triangles to Digraph
    verts = par.get_vertices() #parent vertices counter-clockwise
    #new triangles -> already counter-clockwise
    new_t1 = Node(verts[0],verts[1], pt)
    new_t2 = Node(verts[1],verts[2], pt)
    new_t3 = Node(verts[2],verts[0], pt)
    DG.add_node(new_t1)
    DG.add_node(new_t2)
    DG.add_node(new_t3)
    DG.add_edge(par, new_t1)
    DG.add_edge(par, new_t2)
    DG.add_edge(par, new_t3)

    # updates the DCEL
    h1_1 = hedge(verts[1], pt)
    h1_2 = hedge(pt, verts[0])
    h1_3 = dcel.get_hedge((verts[0], verts[1]))
    h1_1.set_data(new_t1, h1_3, h1_2)
    h1_2.set_data(new_t1, h1_1, h1_3)
    h1_3.set_data(new_t1, h1_2, h1_1)
    dcel.add_hedge(h1_1)
    dcel.add_hedge(h1_2)

    h2_1 = hedge(verts[2], pt)
    h2_2 = hedge(pt, verts[1])
    h2_3 = dcel.get_hedge((verts[1], verts[2]))
    h2_1.set_data(new_t2, h2_3, h2_2)
    h2_2.set_data(new_t2, h2_1, h2_3)
    h2_3.set_data(new_t2, h2_2, h2_1)
    dcel.add_hedge(h2_1)
    dcel.add_hedge(h2_2)

    h3_1 = hedge(verts[0], pt)
    h3_2 = hedge(pt, verts[2])
    h3_3 = dcel.get_hedge((verts[2], verts[0]))
    h3_1.set_data(new_t3, h3_3, h3_2)
    h3_2.set_data(new_t3, h3_1, h3_3)
    h3_3.set_data(new_t3, h3_2, h3_1)
    dcel.add_hedge(h3_1)
    dcel.add_hedge(h3_2)

    dcel.get_hedge((verts[2], pt)).face.draw()
    dcel.get_hedge((verts[1], pt)).face.draw()
    dcel.get_hedge((verts[0], pt)).face.draw()
    control.sleep()
    dcel.get_hedge((verts[2], pt)).face.remove_draw()
    dcel.get_hedge((verts[1], pt)).face.remove_draw()
    dcel.get_hedge((verts[0], pt)).face.remove_draw()

    for he in [h1_1, h2_1, h3_1]:
        if he.face != he.next.face or\
            he.face != he.prev.face:
            print ("BIG PROBLEM NUMBER 2")

    return [new_t1, new_t2, new_t3]


# edge[0]---pt---edge[1]
# \------other----/
def update_DG_special_case (pt, dir_edge):
    global DG, dcel

    # Updates DG
    he = dcel.get_hedge(dir_edge)
    other_vert = he.next.destine
    f = he.face
    f_beg = Node(he.origin, pt, other_vert)
    f_end = Node(pt, he.destine, other_vert)
    DG.add_node(f_beg)
    DG.add_node(f_end)
    DG.add_edge(f, f_beg)
    DG.add_edge(f, f_end)
    return other_vert, f_beg, f_end

def update_DCEL_special_case (
        he_prev, he_next,
        ver, pt,
        face_beg, face_end):
    he_beg = hedge(he_prev.destine, pt, face_beg, prev=he_prev)
    he_end = hedge(pt, he_next.origin, face_end, nxt=he_next)
    t_divider_1 = hedge(pt, ver, face_beg, he_beg, he_prev)
    t_divider_2 = hedge(ver, pt, face_end, he_next, he_end)
    he_beg.next  = t_divider_1
    he_end.prev  = t_divider_2

    he_prev.prev = t_divider_1
    he_prev.next = he_beg
    he_prev.face = face_beg

    he_next.next = t_divider_2
    he_next.prev = he_end
    he_next.face = face_end

    dcel.add_hedge(he_beg)
    dcel.add_hedge(he_end)
    dcel.add_hedge(t_divider_1)
    dcel.add_hedge(t_divider_2)

    for he in [t_divider_1, t_divider_2]:
        if he.face != he.next.face or\
            he.face != he.prev.face:
            print ("BIG PROBLEM NUMBER 3")

def add_to_degenerated (par, pt):
    global dcel, DG
    edge_contains = None
    if on_segment(par.v1, par.v2, pt):
        edge_contains = (par.v1, par.v2)
    elif on_segment(par.v2, par.v3, pt):
        edge_contains = (par.v2, par.v3)
    elif on_segment(par.v3, par.v1, pt):
        edge_contains = (par.v3, par.v1)
    else:
        print("ERRO, NAO ERA DEGENERADO")

    # Updates DG
    edge_twin = (edge_contains[1], edge_contains[0])
    ver1, f1_beg, f1_end = update_DG_special_case(pt, edge_contains)
    ver2, f2_beg, f2_end = update_DG_special_case(pt, edge_twin)
    f1_beg.draw()
    f1_end.draw()
    f2_beg.draw()
    f2_end.draw()
    control.sleep()
    f1_beg.remove_draw()
    f1_end.remove_draw()
    f2_beg.remove_draw()
    f2_end.remove_draw()


    # Updates dcel
    he1 = dcel.get_hedge(edge_contains)
    he2 = dcel.get_hedge(edge_twin)
    he2_prev = he2.prev
    he2_next = he2.next
    he1_prev = he1.prev
    he1_next = he1.next
    dcel.remove_edge(edge_contains[0], edge_contains[1])

    # first triangle subdivision
    update_DCEL_special_case(
        he1_prev, he1_next,
        ver1, pt,
        f1_beg, f1_end)
    # second triangle subdivision
    update_DCEL_special_case(
        he2_prev, he2_next,
        ver2, pt,
        f2_beg, f2_end)

    return [f1_beg, f1_end, f2_beg, f2_end]


def find_destine(pt):
    global DG, root
    visited = set()
    stack = [root]
    visited.add(root)
    found = None
    while (found is None):
        node = stack[-1]
        if (node in visited):
            node.draw()
            control.sleep()
            f = False
            for nd in DG.adj[node]:
                if (nd not in visited):
                    node.remove_draw()
                    stack.append(nd)
                    f = True
                    break
            if (f): continue
            #At this point: node is the leaf!
        else:
            if not node.contains_proper(pt) and not node.is_on_edge(pt):
                # node subtree does not contain pt
                stack.pop()
            visited.add(node)
            continue
        found = node
    found.remove_draw()
    degen = found.is_on_edge(pt)
    return degen, found

def fix_illegal(to_fix):
    global DG, dcel
    frontier = set() # set of edges that needs fixing
    fixed = set() # set of fixed edges
    for t in to_fix:
        for e in t.get_edges():
            if (e[1],e[0]) not in frontier:
                frontier.add(e)
    while (len(frontier) > 0):
        did = None
        e = frontier.pop()
        he1 = dcel.get_hedge(e)
        he2 = dcel.get_hedge((e[1], e[0])) # twin of e1
        f1 = he1.face
        f2 = he2.face
        if he1.face is None or he2.face is None: #outer triangle
            pass
        elif he1.face.needs_fix(he2.face):
            he1_nxt = he1.next
            he2_nxt = he2.next
            dcel.remove_edge(e[0], e[1])
            
            # new triangles maintained counter-clockwise
            n_t1 = Node(e[1], he1_nxt.destine, he2_nxt.destine)
            n_t2 = Node(e[0], he2_nxt.destine, he1_nxt.destine)

            # updates DAG
            DG.add_node(n_t1)
            DG.add_node(n_t2)
            DG.add_edge(f1, n_t1)
            DG.add_edge(f1, n_t2)
            DG.add_edge(f2, n_t1)
            DG.add_edge(f2, n_t2)

            # updates DCEL
            n_he1 = hedge(he1_nxt.destine, he2_nxt.destine, n_t1,\
                          he1_nxt, he1_nxt.prev)
            n_he1.next.prev = n_he1
            n_he1.prev.next = n_he1
            n_he1.prev.face = n_t1
            n_he1.next.face = n_t1
            n_he2 = hedge(he2_nxt.destine, he1_nxt.destine, n_t2,\
                          he2_nxt, he2_nxt.prev)
            n_he2.next.prev = n_he2
            n_he2.prev.next = n_he2
            n_he2.prev.face = n_t2
            n_he2.next.face = n_t2

            dcel.add_hedge(n_he1)
            dcel.add_hedge(n_he2)

            n_t1.draw()
            n_t2.draw()
            did = control.plot_segment(n_he1.origin.x, n_he1.origin.y,\
              n_he1.destine.x, n_he1.destine.y, color="#ffffff")
            control.sleep()
            control.plot_delete(did)
            n_t1.remove_draw()
            n_t2.remove_draw()
            # adds new illegal checks
            for e in n_t1.get_edges():
                if (e[1],e[0]) not in frontier:
                    frontier.add(e)
            for e in n_t2.get_edges():
                if (e[1],e[0]) not in frontier:
                    frontier.add(e)

            if n_he1.face != n_he1.next.face or\
               n_he1.face != n_he1.prev.face or\
               n_he2.face != n_he2.next.face or\
               n_he2.face != n_he2.prev.face:
               print ("BIG PROBLEM")


def triangulation (points):
    global DG, root, dcel
    points = list(set(points))
    pre_process(points)
    for pt in points:
        pt.hilight(color='#00ff00')
        # encontra onde pt esta em DG
        is_degen, node = find_destine (pt)
        # Adiciona pt e as tres novas arestas
        if is_degen:
            n_leafs = add_to_degenerated(node, pt)
        else:
            n_leafs = add_to_normal_case (node, pt)
        #legaliza as arestas de DG
        fix_illegal(n_leafs)
        pt.hilight(color='#00ffff')
    post_process()
    drawn = set()
    for he in dcel.hedges.values():
        if not he.face in drawn and he.face is not None:
            drawn.add(he.face)
            he.face.draw()
    control.sleep()
    for face in drawn:
        face.remove_draw()
    
    return DG, dcel

