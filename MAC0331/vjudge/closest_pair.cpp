#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include <iomanip>
#include <algorithm>

struct point {
    float x;
    float y;
    point(){}
    point (float xi, float yi) {x = xi; y = yi;}
    inline void cp (point&other) {x = other.x; y = other.y;}
};
bool cmpX (const point& t, const point& other) {return t.x < other.x;}
bool cmpY (const point& t, const point& other) {return t.y < other.y;}
inline void swap (std::vector<point>& pts, int i, int j) {
    float x = pts[i].x;
    float y = pts[i].y;
    pts[i].cp(pts[j]);
    pts[j].x = x; pts[j].y = y;
}
float dist (point &p1, point &p2) {
    return sqrt(std::pow(p1.x - p2.x, 2.0f) + std::pow(p1.y-p2.y, 2.0f));
}

void interleave (std::vector<point>& pts, int min, int mid, int max,
        std::vector<point>& buffer) {
    std::merge(pts.begin() + min, pts.begin() + mid + 1, pts.begin() + mid + 1,
        pts.begin() + max + 1, buffer.begin(), cmpY);
    for (int i = 0; i <= max - min; ++i)
        pts[min + i].cp(buffer[i]);
}

float verify_line(std::vector<point> &pts, int min, int max, float midX,
        float min_d, std::vector<point> &buffer) {
    float ref = midX;
    int buf_ind = min;
    for (int i = min; i <= max; ++i) 
        if (std::abs(pts[i].x - ref) < min_d)
            buffer[buf_ind++].cp(pts[i]);
    --buf_ind;
    for (int i = min; i < buf_ind; ++i) {
        int aux = std::min(buf_ind - i, 7);
        for (int j = i + 1; j <= i + aux; ++j)
            min_d = std::min(min_d, dist(buffer[i], buffer[j]));
    }
    return min_d;
}

float min_dist (std::vector<point> &pts, int min, int max,
        std::vector<point> &buffer) {
    // pts[min].x <= pts[min+1].x .... <= pts[max].x
    int d = max - min;
    if (d == 2) {
        float m = std::min(dist(pts[min], pts[min+1]),
             dist(pts[min], pts[max]));
        m = std::min(m, dist(pts[min+1], pts[max]));
        std::sort(pts.begin() + min, pts.begin() + max + 1, cmpY);
        return m;
    }
    else if (d == 1) {
        if (pts[min].y > pts[max].y)
            swap(pts, min, max);
        return dist(pts[min], pts[max]);
    }
    int mid = (min + max)/2;
    float midX = pts[mid].x;
    float ml = min_dist (pts, min, mid, buffer);
    // pts[min].y <= pts[min+1].y <= .... <= pts[mid].y
    float mr = min_dist (pts, mid+1, max, buffer);
    // pts[mid+1].y <= pts[mid+2].y <= .... <= pts[max].y
    interleave(pts, min, mid, max, buffer);
    // pts[min].y <= pts[min+1].y <= .... <= pts[max].y
    float m = std::min(ml, mr);
    float ln = verify_line(pts, min, max, midX, m, buffer);
    return ln;
}

int main() {
    std::vector<point> points;
    std::vector<point> buffer;
    int n;
    float minD, x, y;
    float max = pow(10.0, 4.0);
    for (std::cin >> n; n != 0; std::cin >> n) {
        minD = std::numeric_limits<float>::max();
        for (int i = 0; i < n; ++ i) {
            std::cin >> x >> y;
            points.push_back({x,y});
        }
        buffer = std::vector<point>{n};
        std::sort(points.begin(), points.end(), cmpX);
        minD = min_dist(points, 0, n-1, buffer);
        if (minD < max)
            std::cout << std::setprecision(4) << std::fixed 
                << minD << "\n";
        else
            std::cout << "INFINITY\n";
        points.clear();
    }
    return 0;
}