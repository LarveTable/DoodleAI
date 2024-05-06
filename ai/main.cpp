#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // Include this header for automatic conversions of std::vector
#include "game_state.h"
#include "ai_classes.h"

namespace py = pybind11;

PYBIND11_MODULE(main, m) {
    m.doc() = "DoodleJump AI by Yorick Charlery"; // optional module docstring

    py::class_<AIGeneration>(m, "AIGeneration")
        .def(py::init<int, std::vector<double>>())
        .def(py::init<AIGeneration*>())
        .def("sortPlayers", &AIGeneration::sortPlayers)
        .def("mutatePlayers", &AIGeneration::mutatePlayers)
        .def("__repr__", &AIGeneration::printPlayers)
        .def("getPlayers", &AIGeneration::getPlayers)
        .def_readwrite("players", &AIGeneration::players);

    py::class_<AIPlayer>(m, "AIPlayer")
        .def(py::init<int, std::vector<double>>())
        .def("makeMove", &AIPlayer::makeMove)
        .def_readwrite("identifier", &AIPlayer::identifier)
        .def_readwrite("lastMove", &AIPlayer::lastMove)
        .def_readwrite("weights", &AIPlayer::weights)
        .def_readwrite("state", &AIPlayer::state)
        .def_readwrite("fitness", &AIPlayer::fitness)
        .def("getWeights", &AIPlayer::getWeights)
        .def_readwrite("nearestId", &AIPlayer::nearestId);

    py::class_<State>(m, "State")
        .def(py::init<>())
        .def_readwrite("playerPos", &State::playerPos)
        .def_readwrite("playerVel", &State::playerVel)
        .def_readwrite("score", &State::score)
        .def_readwrite("platforms", &State::platforms)
        .def_readwrite("touchedPlatforms", &State::touchedPlatforms)
        .def_readwrite("lastTouchedPlatform", &State::lastTouchedPlatform);

    py::class_<Platform>(m, "Platform")
        .def(py::init<>())
        .def_readwrite("x", &Platform::x)
        .def_readwrite("y", &Platform::y)
        .def_readwrite("width", &Platform::width)
        .def_readwrite("id", &Platform::id);
}