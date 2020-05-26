#include <iostream>
#include <vector>
#include <algorithm>

struct point {
    double x;
    double y;
    point (double xi, double yi) {x = xi; y = yi;}
    inline void cp (point&other) {x = other.x; y = other.y;}
};
bool cmpX (const point& t, const point& other) {return t.x < other.x;}
bool cmpY (const point& t, const point& other) {return t.y < other.y;}
bool cmp  (const point& t, const point& other) {
    double xdiff = t.x - other.x;
    if (xdiff == 0.0) {
        return t.y < other.y;
    }
    return xdiff < 0.0;
}   

int main() {
    std::vector<point> points;
    int n;
    double x, y;
    bool flag;
    for (std::cin >> n; n != 0; std::cin >> n) {
        flag = false;
        for (int i = 0; i < n; ++ i) {
            std::cin >> x >> y;
            points.push_back({x,y});
        }
        std::sort(points.begin(), points.end(), cmp);
        for (int i = 0; i < points.size(); i += 2) {
            // at least two have the same (x,y) => points[i] == points[i+1]
            if (points[i].x == points[i+2].x) {
                if (points[i].y == points[i+2].y) {
                    flag = true;
                    break;
                }
            }
        }
        if (flag)
            std::cout << "NO\n";
        else
            std::cout << "YES\n";
        points.clear();
    }
    return 0;
}