import pygame
import pymunk

class Player:
    def __init__(self, x, y, texture, window, sim):
        self.sim = sim
        self.window = window
        self.space = sim.space
        self.body = pymunk.Body()
        self.body.position = x, y
        self.body.mass = 0.1
        self.radius = 30
        self.texture = pygame.transform.scale(texture, (4*self.radius, 4*self.radius))
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = 1 # Will be used to calculate mass of the body knowing the shape and density
        self.shape.elasticity = 1
        self.shape.collision_type = 1
        self.shape.filter = pymunk.ShapeFilter(group=1)
        self.space.add(self.body, self.shape)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move(self.body.position.x-8, self.body.position.y)
        if keys[pygame.K_RIGHT]:
            self.move(self.body.position.x+8, self.body.position.y)
        if keys[pygame.K_SPACE]:
            self.body.velocity = 0, 0
            self.move(250, 200)
        """if keys[pygame.K_UP]:
            self.move(self.body.position.x, self.body.position.y+5)
        if keys[pygame.K_DOWN]:
            self.move(self.body.position.x, self.body.position.y-5)""" # Useless and may cause bugs

    def draw(self):
        collision_handler = self.space.add_collision_handler(1, 2)
        collision_handler.begin = self.handle_collision
        self.body.velocity = 0, self.body.velocity.y
        if (self.body.velocity.y > 0):
            self.shape.filter = pymunk.ShapeFilter(group=2)
        else:
            self.shape.filter = pymunk.ShapeFilter(group=1)
        x, y = self.body.position
        x, y = self.sim.convert_coordinates(x, y)
        pygame.draw.circle(self.window, (0, 0, 255), (int(x), int(y)), self.radius) # Converting to int because pygame doesn't accept floats
        self.window.blit(self.texture, (int(x)-2*self.radius, int(y)-2*self.radius)) # Blit the texture to the window

    def move(self, x, y):
        self.body.position = x, y

    def handle_collision(self, arbiter, space, data):
        self.body.velocity = 0, 850
        return True
    
    def get_position(self):
        return self.body.position
