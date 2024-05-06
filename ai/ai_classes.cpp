#include "game_state.h"
#include "ai_classes.h"

#include <cstdlib> // for rand() and srand()
#include <ctime>   // for seeding the random number generator
#include <iostream> // for std::cout
#include <random> // for std::random_device and std::mt19937
#include <cmath> // for std::sqrt

//Idea for the movement value : the final result should be the result devrait etre multiplié à chaque fois par la valeur des poids et comme ça par exemple l'heuristique pour si le perso est au dessus de la plateforme ferait s'écraser le mouvement si la plateforme permet de gagner en score
//compute next movement score and try variations and keep the best for example the distance between the player and the platform decreases

int AIPlayer::makeMove(){

    int capped = 10;

    // Seed the random number generator
    srand(time(nullptr));

    int correction = rand() % 200;

    srand(identifier + correction*correction); // seed the random number generator with the player's identifier

    // Generate a random integer between -4 and 4
    int move_value = rand() % 9 - 4; // generates a random integer in the range [-4, 4]

    if (move_value == 0) {
        move_value = 1;
    }

    Platform nearest = computeNearestPlatform();
    double distance = computeDistanceToPlatform(nearest);

    //heuristic one
    move_value += (distance/20)*weights[0]; 

    if(distance < 0 && move_value > 0){
        move_value *= -1;
    }
    else if (distance > 0 && move_value < 0){
        move_value *= -1;
    }

    double ninja = computeNinjaDistanceToPlatform(nearest, distance);

    //heuristic two
    move_value += ninja*weights[1];

    double close = closeCall(nearest);

    //heuristic three
    move_value += close*weights[2];

    if (std::abs(move_value) > capped){
        if (move_value > 0){
            move_value = capped;
        }
        else{
            move_value = -capped;
        }
    }

    lastMove = move_value; // store the last move

    return move_value;
}

double AIPlayer::closeCall(const Platform& platform){
    double close = 0;
    if (platform.y == -1 && state.playerPos[1] > state.lastTouchedPlatform.y){
        close = computeDistanceToPlatform(state.lastTouchedPlatform);
        return close/5;
    }
    return 0;
}

Platform AIPlayer::computeNearestPlatform(){
    Platform nearestPlatform;
    nearestPlatform.y = -1; // generic
    nearestPlatform.x = 0; // generic
    nearestPlatform.id = -1; // generic
    double minDistance = std::numeric_limits<double>::max(); // initialize the minimum distance to a large value

    // Iterate over all platforms in the game state
    for (const Platform& platform : state.platforms) {
        if (platform.id != state.lastTouchedPlatform.id) {
            // Check if the platform is below the player's y value
            if (platform.y < state.playerPos[1]) {
                if (platform.y > nearestPlatform.y){
                    // Calculate the distance between the player and the platform
                    double distance = std::sqrt(std::pow(platform.x - state.playerPos[0], 2) + std::pow(platform.y - state.playerPos[1], 2));
                    // Update the nearest platform if the distance is smaller than the current minimum distance
                    if (distance < minDistance) {
                        minDistance = distance;
                        nearestPlatform = platform;
                    }
                }
            }
        }
    }
    nearestId = nearestPlatform.id;

    return nearestPlatform;
}

double AIPlayer::computeDistanceToPlatform(const Platform& platform){
    // Calculate the distance between the player and the platform in the x axis
    double distance = platform.x - state.playerPos[0];
    return distance;
}

double AIPlayer::computeNinjaDistanceToPlatform(const Platform& platform, double distance){
    double ninja = 0;
    if (distance < 0) {
        ninja = 500 - state.playerPos[0] + platform.x;
    }
    else{
        ninja = -(500 - platform.x + state.playerPos[0]);
    }

    if (std::abs(ninja) < distance){
        return ninja;
    }
    else{
        return 0;
    }
}

void AIPlayer::evaluatePlayer(){
    
    int result = 0;

    result += state.score;

    


    fitness = result;

}

std::vector<double> AIPlayer::getWeights(){
    return weights;
}

void AIGeneration::sortPlayers(){
    // Sort the players based on their total score
    for(int i = 0; i < size; i++){
        for(int j = i + 1; j < size; j++){
            if(players[i].state.score < players[j].state.score){
                AIPlayer temp = players[i];
                players[i] = players[j];
                players[j] = temp;
            }
        }
    }
}

void AIGeneration::mutatePlayers(){
    // Seed the random number generator
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> dis(-0.5f, 0.5f);

    for(int i = 0; i < size; i++){
        for(int j = 0; j < players[i].weights.size(); j++){

            // Generate a random float between -0.5 and 0.5
            float random_float = dis(gen);

            // Apply the mutation to the weights
            players[i].weights[j] += random_float;
        }
    }
}

std::string AIGeneration::printPlayers(){
    // player name, score, last move, weights
    std::string output = "";
    for (int i = 0; i < size; i++) {
        output += "Player " + std::to_string(players[i].identifier) + ": ";
        output += "Score: " + std::to_string(players[i].state.score) + ", ";
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