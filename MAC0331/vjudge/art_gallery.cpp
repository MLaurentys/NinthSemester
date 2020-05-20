#include <iostream>
#include <vector>

struct point {
    int x;
    int y;
    point (int xi, int yi) {x = xi; y = yi;}
};

// is p3 to the left of (p1-p2)
int area_2 (point p1, point p2, point p3) {
    return p1.x*p2.y - p1.y*p2.x + p1.y*p3.x
          -p1.x*p3.y + p2.x*p3.y - p3.x*p2.y;
}

int main() {
    bool clock, counterclock, ret;
    std::vector<point> borders;
    int n, x, y, a, b, c;
    int area;
    for (std::cin >> n; n != 0; std::cin >> n) {
        clock = counterclock = ret = false;
        for (int i = 0; i < n; ++ i) {
            std::cin >> x >> y;
            borders.push_back({x,y});
        }
        for (int i = 0; i < n; ++i) {
            a = i;
            b = (i + 1) % n;
            c = (i + 2) % n;
            area = area_2(borders[a],borders[b],borders[c]);
            if (area < 0.0f)
                counterclock = true;
            else if (area > 0.0f)
                clock = true;
            if (clock && counterclock)
                ret = true;
        }
        if (ret)
            std::cout << "Yes\n";
        else
            std::cout << "No\n";
        borders.clear();
    }

    return 0;
}