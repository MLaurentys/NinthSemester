from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config
from geocomp import colors

def swap (lst, i1, i2):
    tmp = lst[i1]
    lst[i1] = lst[i2]
    lst[i2] = tmp

def extreme_point (points, start, end):
    area = -1.0
    ind = -1
    for i in range (start+1, end):
        n_area = prim.area2(points[start], points[end], points[i])
        if area < n_area:
            ind = i
            area = n_area
    return ind

def partition (points, start, end):
    pt_ind = extreme_point(points, start, end)
    swap(points, start + 1, pt_ind)
    part1 = part2 = end
    for i in range (end-1, start+1, -1):
        if prim.left(points[start], points[start+1], points[i]):
            part1 -= 1
            swap(points, part1, i)
        elif prim.left(points[start+1], points[end], points[i]):
            part1 -= 1
            part2 -= 1
            swap(points, part2, i)
            if part1 != part2: 
                swap(points, part1, i)
    part1 -= 1
    part2 -= 1
    swap(points, part2, start + 1)
    if part1 != part2:
        swap(points, part1, start+1)
    part1 -= 1
    swap (points, part1, start)
    return part1, part2

def hilight_rec_call(points, start, end, part1, part2):
    for pt in points[start:part1]:
        pt.hilight("yellow")
    for pt in points[part1:part2]:
        pt.hilight("green")
    for pt in points[part2:end+1]:
        pt.hilight("red")
    draw_triang(points[part1], points[part2], points[end])
    for pt in points[start:end+1]:
        pt.unhilight()

def draw_triang(pt1, pt2, pt3):
    seg1 = segment.Segment(pt1, pt2)
    seg2 = segment.Segment(pt1, pt3)
    seg3 = segment.Segment(pt2, pt3)
    seg1.hilight("yellow")
    seg2.hilight("yellow")
    seg3.hilight("yellow")
    control.sleep()
    seg1.unhilight()
    seg2.unhilight()
    seg3.unhilight()

# returns a list of the points that belong to the convex hull of points[start:end+1]
def q_hull_rec (points, start, end):
    if end - start == 1: # two points
        ret_val = set([points[end], points[start]])
    else:
        part1, part2 = partition(points, start, end)
        #hilights points in current recursive call
        hilight_rec_call(points, start, end, part1, part2)
        res1 = q_hull_rec(points, part1, part2)
        res2 = q_hull_rec(points, part2, end)
        ret_val = res1.union(res2)
    # treats degenerated case
    if len(ret_val) == 3:
        ret_val = list(ret_val)
        if prim.collinear(ret_val[0], ret_val[1], ret_val[2]):
            if prim.on_segment(ret_val[0], ret_val[1], ret_val[2]):
                ret_val = set([ret_val[0], ret_val[1]])
            elif prim.on_segment(ret_val[0], ret_val[2], ret_val[1]):
                ret_val = set([ret_val[0], ret_val[2]])
            else:
                ret_val = set([ret_val[1], ret_val[2]])
        else:
            ret_val = set(ret_val)
    return ret_val

# returns a list of the points that belong to the convex hull of points 
def q_hull (points):
    n = len(points)
    if n == 1:
        return set(points)
    f_ind = 0
    for i, pt in enumerate(points):
        if pt.y < points[f_ind].y or\
            (pt.y == points[f_ind].y and pt.x < points[f_ind].x):
            f_ind = i
    swap(points, 0, f_ind)
    s_ind = 1
    for i in range(1, len(points)):
        if prim.right(points[0], points[s_ind], points[i]) or\
           (prim.collinear(points[0], points[s_ind], points[i]) and\
            (prim.dist2(points[0], points[s_ind]) <
                prim.dist2(points[0], points[i]))):
            s_ind = i
    swap(points, n-1, s_ind)
    hull = q_hull_rec(points, 0, n-1)
    for pt in hull: pt.hilight("blue")
    return hull
