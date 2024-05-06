class AInstance:
    def __init__(self, gen, player):
        self.gen = gen
        self.player = player

    def update_state(self, game):
        self.player.state = game.get_state() #Maybe put the state as a class variable

    def make_move(self):
        move = self.player.makeMove()
        return move
    
    def get_nearest_platform(self):
        return self.player.nearestId