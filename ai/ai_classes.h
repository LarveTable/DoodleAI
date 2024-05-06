#ifndef ai_classes_h
#define ai_classes_h

#include "game_state.h"
#include <vector>

class AIPlayer {
    public: // make attributes private later
        AIPlayer(int identifier, const std::vector<double>& weights) 
        : identifier(identifier), lastMove(0), weights(weights) {};
        AIPlayer(){}; // Default constructor
        int identifier;
        int lastMove;
        std::vector<double> weights;
        void evaluatePlayer();
        int makeMove();
        State state;
        int fitness;
        std::vector<double> getWeights();
        Platform computeNearestPlatform();
        double computeDistanceToPlatform(const Platform& platform);
        long nearestId;
        double computeNinjaDistanceToPlatform(const Platform& platform, double distance);
        double closeCall(const Platform& platform);

};

class AIGeneration {
    public:
        AIGeneration(int size, const std::vector<double>& weights) : size(size) {
        players.reserve(size);
        for (int i = 0; i < size; ++i) {
            players.emplace_back(i, weights);
        }
        };
        AIGeneration(AIGeneration* previous) : size(previous->size) {
        players.reserve(size);
        for (int i = 0; i < size; ++i) {
            players.emplace_back(previous->players[i]);
        }
        };
        int size;
        std::vector<AIPlayer> players;
        void sortPlayers();
        void mutatePlayers();
        std::string printPlayers();
        std::vector<AIPlayer> getPlayers();
};

#endif // ai_classes_h