from geocomp.common import prim
from geocomp.common import segment

##
## Functions reponsible for calculating intersections
##
def is_below(s1, s1_k, s2, s2_k):
    if s1.has_left(s2_k):return True
    if s2.has_left(s1_k):return False
    if s1.value.has_left(s2.to): return True
    return False

def area2 (p1, p2, p3):
    return p1.x*p2.y - p1.y*p2.x + p1.y*p3.x \
            -p1.x*p3.y + p2.x*p3.y - p3.x*p2.y
# p2 to the left of segment (pt,p1)
def at_left(pt, p1, p2):
    return area2 (pt,p1,p2) > 0
def is_colinear (p1,p2,p3):
    return area2(p1,p2,p3) == 0
# Whether pt is in between p1 and p2 (presumes p1 <= p2)
def in_between(pt, p1, p2):
    ret = False
    if is_colinear(pt,p1,p2):
        if p1.x != p2.x:
            ret = p1.x <= pt.x <= p2.x
        else:
            ret = p1.y <= pt.y <= p2.y
    return ret

# Whether segmets cross in one midpoint
def seg_intersects_properly (seg1, seg2):
    a,b,c,d = seg1.init, seg1.to, seg2.init, seg2.to
    if is_colinear(a,c,d) or \
        is_colinear(b,c,d) or \
        is_colinear(c,a,b) or \
        is_colinear(d,a,b):
        return False
    return (at_left(a,c,d) != at_left(b,c,d)) and \
            (at_left(c,a,b) != at_left(d,a,b))

# Get intersection point
def intersection (seg1, seg2):
    def line(p1, p2):
        A = (p1.y - p2.y)
        B = (p2.x - p1.x)
        C = (p1.x*p2.y - p2.x*p1.y)
        return A, B, -C
    l1 = line(seg1.init, seg1.to)
    l2 = line(seg2.init, seg2.to)
    d = l1[0]*l2[1] - l1[1]*l2[0]
    dx = l1[2]*l2[1] - l1[1]*l2[2]
    dy = l1[0] * l2[2] - l1[2] * l2[0]
    x = dx/d
    y = dy/d
    return x,y

# Whether segments cross
def seg_intersects(seg1, seg2):
    a,b,c,d = seg1.init, seg1.to, seg2.init, seg2.to
    return prim.intersect(a,b,c,d)
    if (seg_intersects_properly(seg1, seg2)):
        return True
    return in_between(a,c,d) or in_between(b,c,d) or \
            in_between(c,a,b) or in_between(d,a,b)
