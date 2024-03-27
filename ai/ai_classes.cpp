#include "game_state.h"
#include "ai_classes.h"

#include <cstdlib> // for rand() and srand()
#include <ctime>   // for seeding the random number generator
#include <iostream> // for std::cout

int AIPlayer::makeMove(State state){
    // Seed the random number generator
    srand(time(nullptr));

    // Generate a random integer between -4 and 4
    int random_int = rand() % 9 - 4; // generates a random integer in the range [-4, 4]

    // Apply weights to bias the random number
    random_int *= weights[0]; // adjust the random number based on weights

    lastMove = random_int; // store the last move

    // Return the random integer value
    return random_int;
}

int AIPlayer::getScore(){
    return totalScore;
}

std::vector<double> AIPlayer::getWeights(){
    return weights;
}

void AIGeneration::sortPlayers(){
    // Sort the players based on their total score
    for(int i = 0; i < size; i++){
        for(int j = i + 1; j < size; j++){
            if(players[i].getScore() < players[j].getScore()){
                AIPlayer temp = players[i];
                players[i] = players[j];
                players[j] = temp;
            }
        }
    }
}

void AIGeneration::mutatePlayers(){
    // Seed the random number generator
    srand(time(nullptr));

    // Mutate the weights of the top 10% of players
    for(int i = 0; i < size; i++){
        for(int j = 0; j < 1; j++){
            // Generate a random integer between -5 and 5
            int random_int = rand() % 11 - 5; // generates a random integer in the range [-5, 5]

            // Apply the mutation to the weights
            players[i].weights[j] += random_int;
        }
    }
}

std::string AIGeneration::printPlayers(){
    // player name, score, last move, weights
    std::string output = "";
    for (int i = 0; i < size; i++) {
        output += "Player " + std::to_string(players[i].identifier) + ": ";
        output += "Score: " + std::to_string(players[i].totalScore) + ", ";
        output += "Last Move: " + std::to_string(players[i].lastMove) + ", ";

        // Iterate over the weights vector for each player
        output += "Weights: ";
        for (double weight : players[i].weights) {
            output += std::to_string(weight) + ", ";
        }
        output += "\n";
    }
    return output;
}

std::vector<AIPlayer> AIGeneration::getPlayers(){
    return players;
}