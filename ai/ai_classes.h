#ifndef ai_classes_h
#define ai_classes_h

#include "game_state.h"
#include <vector>

class AIPlayer {
    public: // make attributes private later
        AIPlayer(int identifier, const std::vector<double>& weights) 
        : identifier(identifier), totalScore(0), lastMove(0), weights(weights) {};
        AIPlayer(){}; // Default constructor
        int identifier;
        int totalScore;
        int lastMove;
        std::vector<double> weights;
        int makeMove(State state);
        int getScore();
        std::vector<double> getWeights();
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