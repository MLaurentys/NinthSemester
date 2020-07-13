# Gets intersection point
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

def compare_segments(s1, s2):
    d1 = compare_points(s1.init, s2.init)
    if (d1 == 0.0):
        return compare_points(s1.to, s2.to)
    return d1

# left before right, then bottom before top
def compare_points(pt1, pt2):
    if(pt1.x == pt2.x):
        return pt1.y - pt2.y
    return pt1.x - pt2.x