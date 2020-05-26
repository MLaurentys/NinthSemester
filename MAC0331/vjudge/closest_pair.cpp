#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include <iomanip>
#include <algorithm>

struct point {
    double x;
    double y;
    point (double xi, double yi) {x = xi; y = yi;}
    inline void cp (point&other) {x = other.x; y = other.y;}
};
bool cmpX (const point& t, const point& other) {return t.x < other.x;}
bool cmpY (const point& t, const point& other) {return t.y < other.y;}
inline void swap (std::vector<point>& pts, int i, int j) {
    double x = pts[i].x;
    double y = pts[i].y;
    pts[i].cp(pts[j]);
    pts[j].x = x; pts[j].y = y;
}
double dist (point p1, point p2) {
    return sqrt(std::pow(p1.x - p2.x, 2.0f) + std::pow(p1.y-p2.y, 2.0f));
}

void interleave (std::vector<point>& pts, int min, int mid, int max,
        std::vector<point>& buffer) {
    std::merge(pts.begin() + min, pts.begin() + mid + 1, pts.begin() + mid + 1,
        pts.begin() + max + 1, buffer.begin(), cmpY);
    for (int i = 0; i <= max - min; ++i)
        pts[min + i].cp(buffer[i]);
}

double verify_line(std::vector<point> &pts, int min, int max, double midX,
        double min_d) {
    double ref = midX;
    std::vector<point> col;
    for (int i = min; i <= max; ++i) 
        if (std::abs(pts[i].x - ref) < min_d)
            col.push_back(pts[i]);
    for (int i = 0; i < col.size() - 1; ++i) {
        double aux = std::min((int)col.size() - i, 7);
        for (int j = i + 1; j < i + aux; ++j)
            min_d = std::min(min_d, dist(col[i], col[j]));
    }
    return min_d;
}

double min_dist (std::vector<point> &pts, int min, int max,
        std::vector<point> &buffer) {
    // pts[min].x <= pts[min+1].x .... <= pts[max].x
    int d = max - min;
    if (d == 2) {
        double m = std::min(dist(pts[min], pts[min+1]),
             dist(pts[min], pts[max]));
        m = std::min(m, dist(pts[min+1], pts[max]));
        std::sort(pts.begin() + min, pts.begin() + max + 1, cmpY);
        return m;
    }
    else if (d == 1) {
        double m = dist(pts[min], pts[max]);
        if (pts[min].y > pts[max].y)
            swap(pts, min, max);
        return m;
    }
    int mid = (min + max)/2;
    double midX = pts[mid].x;
    double ml = min_dist (pts, min, mid, buffer);
    // pts[min].y <= pts[min+1].y <= .... <= pts[mid].y
    double mr = min_dist (pts, mid+1, max, buffer);
    // pts[mid+1].y <= pts[mid+2].y <= .... <= pts[max].y
    interleave(pts, min, mid, max, buffer);
    // pts[min].y <= pts[min+1].y <= .... <= pts[max].y
    double m = std::min(ml, mr);
    double ln = verify_line(pts, min, max, midX, m);
    return ln;
}

int main() {
    std::vector<point> points;
    std::vector<point> buffer;
    std::vector<int> y_ord;
    int n;
    double minD, x, y;
    double max = pow(10.0, 4.0);
    for (std::cin >> n; n != 0; std::cin >> n) {
        minD = std::numeric_limits<double>::max();
        for (int i = 0; i < n; ++ i) {
            std::cin >> x >> y;
            points.push_back({x,y});
            y_ord.push_back(i);
        }
        buffer.reserve(n);
        std::sort(points.begin(), points.end(), cmpX);
        minD = min_dist(points, 0, n-1, buffer);
        if (minD < max)
            std::cout << std::setprecision(4) << std::fixed 
                << minD << "\n";
        else
            std::cout << "INFINITY\n";
        points.clear();
        y_ord.clear();
    }
    return 0;
}