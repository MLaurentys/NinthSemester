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
};
bool cmpX (const point& t, const point& other) {return t.x < other.x;}

double dist2 (point p1, point p2) {
    return std::pow(p1.x - p2.x, 2.0f) + std::pow(p1.y-p2.y, 2.0f);;
}

double verify_line(std::vector<point> &pts, std::vector<int> &y_ord,
        int min, int max, double md) {
    int mid = (min+ max)/2;
    double ref = pts[mid].x;
    std::vector<point> col;
    for (int i = min; i < max; ++i) 
        if (std::abs(pts[y_ord[i]].x - ref) < md)
            col.push_back(pts[y_ord[i]]);
    for (int i = 0; i < col.size(); ++i)
        for (int j = i+1; j < std::min((int)col.size(), i + 8); ++j)
            md = std::min(md, dist2(col[i], col[j]));
    return md;
}

double min_dist (std::vector<point> &pts, std::vector<int> &y_ord, 
        int min, int max) {
    int d = max - min;
    if (d == 2) {
        double m = std::min(dist2(pts[min], pts[min+1]),
             dist2(pts[min], pts[max]));
        return std::min(m, dist2(pts[min+1], pts[max]));
    }
    else if (d == 1) return dist2(pts[min], pts[max]);
    int mid = (min + max)/2;
    double ml = min_dist (pts, y_ord, min, mid);
    double mr = min_dist (pts, y_ord, mid, max);
    double m = std::min(ml, mr);
    double ln = verify_line(pts, y_ord, min, max, m);
    return ln;
}

int main() {
    std::vector<point> points;
    std::vector<int> y_ord;
    int n;
    double minD, x, y;
    double max = pow(10.0, 8.0);
    for (std::cin >> n; n != 0; std::cin >> n) {
        minD = std::numeric_limits<double>::max();
        for (int i = 0; i < n; ++ i) {
            std::cin >> x >> y;
            points.push_back({x,y});
            y_ord.push_back(i);
        }
        std::sort(points.begin(), points.end(), cmpX);
        std::sort(y_ord.begin(), y_ord.end(), [points](int i, int j)
            {return points[i].y < points[j].y;});
            minD = min_dist(points, y_ord, 0, n);
        if (minD < max)
            std::cout << std::setprecision(4) << std::fixed 
                << sqrt(minD) << "\n";
        else
            std::cout << "INFINITY\n";
        points.clear();
        y_ord.clear();
    }

    return 0;
}