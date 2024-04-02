class AInstance:
    def __init__(self, gen, player):
        self.gen = gen
        self.player = player

    def update_state(self, game):
        self.state = game.get_state()
        self.player.totalScore = int(game.score)

    def make_move(self):
        move = self.player.makeMove(self.state)
        return move
    
    def mutate(self):
        self.gen.mutatePlayers()

    def print_players(self):
        print(self.gen)
    
    def print_weights(self):
        print(self.player.getWeights())

    def get_players(self):
        return self.player