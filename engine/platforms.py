import pymunk
import pygame

class Platform:
    def __init__(self, texture, p1, p2, sim, window, color):
        #self.texture = texture
        self.sim = sim
        self.p1 = p1
        self.p2 = p2
        self.thickeness = 5
        self.color = color
        self.color_debug = self.color
        self.window = window
        self.space = sim.space
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Segment(self.body, (p1[0], p1[1]), (p2[0], p2[1]), self.thickeness)
        self.shape.elasticity = 0
        self.shape.filter = pymunk.ShapeFilter(group=2)
        self.space.add(self.body, self.shape) # When using static bodies, we only add the shape to the space

    def draw(self):
        start = self.sim.convert_coordinates(self.p1[0], self.p1[1])
        end = self.sim.convert_coordinates(self.p2[0], self.p2[1])
        pygame.draw.line(self.window, self.color, start, end, 2*self.thickeness) # 10 because pygame expends the thickness of the line to both sides
        self.color = self.color_debug #only for debug

    def move(self, y):
        self.p1 = (self.p1[0], y)
        self.p2 = (self.p2[0], y)
        self.shape.unsafe_set_endpoints(self.p1, self.p2)

    def kill(self):
        self.space.remove(self.shape)

class BasePlatform(Platform):
    def __init__(self, p1, p2, sim, window, color):
        super().__init__('engine/textures/base_platform.png', p1, p2, sim, window, color)
        self.shape.collision_type = 2