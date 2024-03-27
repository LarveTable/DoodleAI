#ifndef game_state_h
#define game_state_h

#include <vector>

struct Platform {
    double x;
    double y;
    double width;
};

struct State {
    std::vector<double> playerPos;
    double playerVel;
    std::vector<Platform> platforms;
};

#endif // game_state_h