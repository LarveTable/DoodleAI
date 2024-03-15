import pymunk

class Simulation:
    def __init__(self, window, fps, font, clock):
        self.space = pymunk.Space()
        self.window = window
        self.fps = fps
        self.font = font
        self.clock = clock
        self.space.gravity = 0, -1500

    def step(self):
        self.clock.tick(self.fps)
        self.space.step(1 / self.fps)

    def convert_coordinates(self, x, y):
        return x, self.window.get_height() - y

    def kill(self):
        # Remove bodies from the space
        for body in self.space.bodies[:]:
            self.space.remove(body)

        # Remove shapes from the space
        for shape in self.space.shapes[:]:
            self.space.remove(shape)

        # Remove constraints from the space
        for constraint in self.space.constraints[:]:
            self.space.remove(constraint)
        del self.space