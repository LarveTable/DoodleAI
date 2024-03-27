import main

class AInstance:
    def __init__(self, game):
        self.game = game
        self.gen = main.AIGeneration(1, [-2.5, 1.7, 2.6])
        self.players = self.gen.getPlayers()

    def update_state(self):
        self.state = self.game.get_state()
        self.get_players()
        for p in self.players:
            p.totalScore = int(self.game.score)

    def make_move(self):
        for p in self.players:
            move = p.makeMove(self.state)
        return move
    
    def mutate(self):
        self.gen.mutatePlayers()

    def print_players(self):
        print(self.gen)
    
    def print_weights(self):
        self.get_players()
        for p in self.players:
            print(p.getWeights())

    def get_players(self):
        self.players = self.gen.getPlayers()