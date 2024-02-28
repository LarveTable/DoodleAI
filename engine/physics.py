import pymunk
import pygame

class Simulation:
    def __init__(self, window, fps, font):
        self.space = pymunk.Space()
        self.window = window
        self.fps = fps
        self.font = font
        self.clock = pygame.time.Clock()
        self.space.gravity = 0, -1500

    def step(self):
        self.clock.tick(self.fps)
        self.space.step(1 / self.fps)

    def convert_coordinates(self, x, y):
        return x, self.window.get_height() - y
    
    def fps_counter(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps, True, pygame.Color("RED"))
        self.window.blit(fps_t,(0,0))