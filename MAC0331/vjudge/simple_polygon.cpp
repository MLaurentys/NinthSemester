#include <iostream>
#include <vector>
#include <algorithm>
#include <memory>
#include <set>
#include <cmath>

struct point;
struct segment;
struct event;

struct point {
    float x;
    float y;
    point (float xi, float yi) {x = xi; y = yi;}
    inline void cp (point&other) {x = other.x; y = other.y;}
};
inline bool cmpX (const point& t, const point& other) {return t.x < other.x;}
inline bool cmpY (const point& t, const point& other) {return t.y < other.y;}
inline bool cmpXY  (const point& t, const point& other) {
    if (t.x == other.x) {
        return t.y < other.y;
    }
    return t.x < other.x;
}
inline float area_tri (const point &a, const point &b, const point &c) {
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x);
}
bool at_left (const point &p1, const point &p2, const point &p3){
    return area_tri(p1, p2, p3) > 0.0f;
}

struct segment {
    point* s;
    point* e;
    int ind;
    segment (point &pt1, point&pt2, int i) {
        s = &pt1; e = &pt2; ind = i;
    }
};
bool on_segment (const segment &seg, const point &p) {
    if (!(area_tri(*seg.s, *seg.e, p) == 0.0f)) return false;
    auto *s = seg.s;
    auto *e = seg.e;
    if (s->x != e->x) {
        return s->x < p.x && p.x < e->x;
    }
    return s->y < p.y && p.y < e->y;
}
struct cmpS{
    bool operator() (const segment *s1, const segment *s2) const {
        //same segment
        if ((s1->s == s2->s) && (s1->e == s2->e)) return false;
        //collinear segments Sx -> Sy -> Ex|y -> Ex|y
        if (area_tri(*s1->s, *s1->e, *s2->s) == 0.0f &&
              area_tri(*s1->s, *s1->e, *s2->e) == 0.0f) {
            return cmpXY(*s1->s, *s2->s);
        }
        if (s1->s == s2->s) {
            return !at_left(*s2->s, *s2->e, *s1->e);
        }
        // starting points in a vertcal line
        if (s1->s->x == s2->s->x) return s1->s->y < s2->s->y;
        if (cmpXY(*s1->s, *s2->s)) // s1->s < s2->s (seg s1 inserted 1st)
            return at_left(*s1->s, *s1->e, *s2->s);
        return !at_left(*s2->s, *s2->e, *s1->s);
    }
};
bool intersect_colinear(const segment& s1, const segment& s2) {
    bool a = (on_segment(s1, *s2.s));
    bool b = (on_segment(s1, *s2.e));
    bool c = (on_segment(s2, *s1.s));
    bool d = (on_segment(s2, *s1.e));
    return  a || b || c || d;
}
bool intersect(const segment& s1, const segment& s2) {
    if (intersect_colinear(s1,s2))
        return true;
    bool a = at_left(*s1.s, *s1.e, *s2.s);
    bool b = at_left(*s1.s, *s1.e, *s2.e);
    bool c = at_left(*s2.s, *s2.e, *s1.s);
    bool d = at_left(*s2.s, *s2.e, *s1.e);
    return (a != b)
      && (c != d);
}

struct event {
    segment *seg;
    point *p;
    int type; // 0 = left, 1 = right
    event (segment &s, point &pt, int tp) {
        seg = &s; type = tp; p = &pt;
    }
};
inline bool eveCmp (const event& e1, const event& e2) {return cmpXY(*e1.p, *e2.p);}

void pre_process (int size, std::vector<point>& pts, std::vector<event>& evts,
        std::vector<segment>& segs) {
    pts.reserve(size);
    evts.reserve(size);
    segs.reserve(size);
    float x, y;
    for (int i = 0; i < size; ++ i) {
        std::cin >> x >> y;
        pts.push_back({x,y});
    }
    for (int i = 0; i < size; ++i) {
        int j = (i+1)%size;
        if (cmpXY(pts[i], pts[j]))
            segs.push_back({pts[i], pts[j], i});
        else
            segs.push_back({pts[j], pts[i], i});
        evts.push_back({segs[i], *segs[i].s, 0});
        evts.push_back({segs[i], *segs[i].e, 1});
    }
    std::sort (evts.begin(), evts.end(), eveCmp);
}

bool seq_handler (std::set<segment*>::iterator it1,
        std::set<segment*>::iterator it2, int sz) {
    int dif = abs((*it1)->ind - (*it2)->ind);
    if (dif > 1 && dif != sz - 1) return true;
    return intersect_colinear(*(*it1), *(*it2));
}



int main() {
    std::ios_base::sync_with_stdio(false); 
    std::cin.tie(NULL); 
    std::cout.tie(NULL);
    std::vector<point> points;
    std::vector<segment> segments;
    std::vector<event> events;
    std::set<segment*,cmpS> tree;
    event *e;
    int n;
    bool flag;
    for (std::cin >> n; n != 0; std::cin >> n) {
        flag = false;
        if (n == 2) flag = true;
        pre_process(n, points, events, segments);
        for (int i = 0; i < (int)events.size(); ++i) {
            e = &events[i];
            if (e->type == 0) {
                if (tree.find(e->seg) != tree.end()) {
                    flag = true;
                    break;
                }
                auto p = std::get<0>(tree.insert(e->seg));
                auto nx = std::next(p);
                if (p != tree.begin() &&
                    seq_handler(std::prev(p), p, n) &&
                    intersect(*(*std::prev(p)), *(*p)))
                    flag = true;
                if (nx != tree.end() &&
                    seq_handler(p, nx, n) &&
                    intersect(*(*nx), *(*p)))
                    flag = true;
            }
            else {
                auto p = tree.find(e->seg);
                if (p != tree.begin() && (next(p) != tree.end()) &&
                    seq_handler(prev(p), next(p), n) &&
                    intersect(*(*next(p)), *(*prev(p))))
                    flag = true;
                tree.erase(p);
            }
            if (flag) break;
        }
        if (flag)
            std::cout << "NO\n";
        else
            std::cout << "YES\n";
        points.clear();
        segments.clear();
        events.clear();
        tree.clear();
    }
    return 0;
}