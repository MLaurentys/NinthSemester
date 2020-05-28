#include <iostream>
#include <vector>
#include <algorithm>
#include <memory>
#include <set>
#include <cmath>

struct point;
struct segment;
struct event;

using p_pt = std::shared_ptr<point>;
using p_seg = std::shared_ptr<segment>;
using p_eve = std::shared_ptr<event>;

struct point {
    float x;
    float y;
    point (float xi, float yi) {x = xi; y = yi;}
    inline void cp (point&other) {x = other.x; y = other.y;}
};
bool cmpX (const point& t, const point& other) {return t.x < other.x;}
bool cmpY (const point& t, const point& other) {return t.y < other.y;}
bool cmpXY  (const point& t, const point& other) {
    float xdiff = t.x - other.x;
    if (xdiff == 0.0) {
        return t.y < other.y;
    }
    return xdiff < 0.0;
}   
float area_tri (const point &a, point &b, const point &c) {
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x);
}
bool at_left (point &p1, point &p2, point &p3){
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
    if (s->x != e->x)
        return s->x <= p.x && p.x <= e->x;
    return s->y <= p.y && p.y <= e->y;
}
bool intersect(const segment& s1, const segment& s2) {
    if (on_segment(s1, *s2.s) || on_segment(s1, *s2.e) ||
        on_segment(s2, *s1.s) || on_segment(s2, *s1.e))
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
bool eveCmp (const event& e1, const event& e2) {return cmpXY(*e1.p, *e2.p);}

void pr_seg(segment &seg){
    std::cout << seg.s->x << " " << seg.s->y << std::endl;
    std::cout << seg.e->x << " " << seg.e->y << std::endl;
}
void pr_eve(event &e){
    std::cout << e.seg->s->x << " " << e.seg->s->y << std::endl;
    std::cout << e.seg->e->x << " " << e.seg->e->y << std::endl;
}
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
        std::cout << 2*i << "\n";
        std::cout << segs[i].s << "\n";
        std::cout << evts[2*i].seg->s << "\n";
    }
    for (int i = 0; i < size; ++i) {
        std::cout << 2*i << "\n";
        std::cout << segs[i].s << "\n";
        std::cout << evts[2*i].seg->s << "\n";
    }
    int i = 0;
    for (event &e : evts){
        std::cout << i++ << "\n";
        pr_eve(e);
    }
    std::sort (evts.begin(), evts.end(), eveCmp);
    i = 0;
    for (event &e : evts){
        std::cout << i++ << "\n";
        std::cout << e.seg->s->x << e.seg->s->y << std::endl;
    }
}

bool not_seq (std::set<segment*>::iterator it1, std::set<segment*>::iterator it2,
              int sz) {
    int dif = abs((*it1)->ind - (*it2)->ind);
    return dif > 1 && dif != sz - 1;
}



int main() {
    std::vector<point> points;
    std::vector<segment> segments;
    std::vector<event> events;
    std::set<segment*> tree;
    event *e;
    int n;
    bool flag;
    for (std::cin >> n; n != 0; std::cin >> n) {
        flag = false;
        pre_process(n, points, events, segments);
        for (int i = 0; i < (int)events.size(); ++i) {
            e = &events[i];
            if (e->type == 0) {
                auto p = std::get<0>(tree.insert(e->seg));
                auto pr = std::prev(p);
                auto nx = std::next(p);
                if (p != tree.begin() &&
                    not_seq(pr, p, n) &&
                    intersect(*(*pr), *(*p)))
                    flag = true;
                if (nx != tree.end() &&
                    not_seq(p, nx, n) &&
                    intersect(*(*nx), *(*p)))
                    flag = true;
            }
            else {
                auto p = tree.find(e->seg);
                if (p != tree.begin() && (next(p) != tree.end()) &&
                    not_seq(prev(p), next(p), n) &&
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