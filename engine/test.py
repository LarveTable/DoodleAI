import main
import numpy as np

test = main.AIGeneration(1, [-2.5, 1.7, 2.6])
players = test.getPlayers()
for p in players:
    print(p.getWeights())

state = main.State()
state.playerPos = [100, 200]
state.playerVel = 200

list = []
for i in range(10):
    p = main.Platform()
    p.x = 100 * i
    p.y = 100 * i
    p.width = 100
    list.append(p)

state.platforms = list

for p in state.platforms:
    #print(p.x, p.y)
    pass

for p in players:
    #print(p.lastMove)
    move = p.makeMove(state)
    #print(move)
    #print(p.lastMove)