class Player:
    def __init__(self):
        self.position = 0

    def move_left(self):
        self.position -= 1

    def move_right(self):
        self.position += 1