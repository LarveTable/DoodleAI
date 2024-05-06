import pygame
import pymunk
import math

class Player:
    def __init__(self, x, y, texture, window, sim, game):
        self.sim = sim
        self.game = game
        self.window = window
        self.space = sim.space
        self.body = pymunk.Body()
        self.body.position = x, y
        self.radius = 30
        self.texture = pygame.transform.scale(texture, (4*self.radius, 4*self.radius))
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = 1 # Will be used to calculate mass of the body knowing the shape and density
        self.shape.elasticity = 0
        self.shape.collision_type = 1
        self.shape.filter = pymunk.ShapeFilter(group=1)
        self.space.add(self.body, self.shape)
        self.position_offset = (self.radius / 2) + 5 # 5 being the platform thickness
        self.velocity_at_zero = 900
        self.body.velocity = 0, 1000
        self.looking = "right"
        self.collision_handler = self.space.add_collision_handler(1, 2)
        self.collision_handler.begin = self.handle_collision
        self.platforms_touched = []
        self.last_touched = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            #self.body.velocity = -500, self.body.velocity.y
            if self.looking == "right":
                self.texture = pygame.transform.flip(self.texture, True, False)
                self.looking = "left"
            self.move(self.body.position.x-8, self.body.position.y)
        if keys[pygame.K_RIGHT]:
            #self.body.velocity = 500, self.body.velocity.y
            if self.looking == "left":
                self.texture = pygame.transform.flip(self.texture, True, False)
                self.looking = "right"
            self.move(self.body.position.x+8, self.body.position.y)
        if keys[pygame.K_SPACE]:
            self.body.velocity = 0, 0
            self.move(250, 200)

    def draw(self):
        if self.body.position.x < 0:
            self.body.position = 500, self.body.position.y
        elif self.body.position.x > 500:
            self.body.position = 0, self.body.position.y  
        self.body.velocity = 0, self.body.velocity.y
        if (self.body.velocity.y > 0):
            self.shape.filter = pymunk.ShapeFilter(group=2)
        else:
            self.shape.filter = pymunk.ShapeFilter(group=1)
        x, y = self.body.position
        x, y = self.sim.convert_coordinates(x, y)
        self.window.blit(self.texture, (int(x)-2*self.radius, int(y)-2*self.radius)) # Blit the texture to the window

    def move(self, x, y):
        self.body.position = x, y

    # Control the player jump
    def handle_collision(self, arbiter, space, data): # trouver un moyen de checker si le joueur collide avec le haut de la plateforme
        if self.body.velocity.y < 0:
            if self.body.position.y - self.radius/2 > arbiter.shapes[1].a[1]:
                state = self.body.position.y
                y = self.required_velocity(state)
                theoritical_height = (self.velocity_at_zero ** 2) / (2 * abs(self.space.gravity[1])) + state
                self.body.velocity = 0, y
                if arbiter.shapes[1] not in self.platforms_touched:
                    self.platforms_touched.append(arbiter.shapes[1])
                if self.last_touched != arbiter.shapes[1]:
                    self.last_touched = arbiter.shapes[1]
                self.game.update_displayed_platforms(y, theoritical_height)
                return True
        return False
        
            # Equations used
            # v^2 = 2g(h-ht)
            # h = v/2g + ht
    
    def get_position(self):
        return self.body.position

    def required_velocity(self, state):
        gravity = self.space.gravity[1]
        height = 400
        
        # Apply equations of motion to find initial velocity
        initial_velocity_squared = 2 * abs(gravity) * (height - state)
        
        # Ensure that the height is achievable with given conditions
        if initial_velocity_squared < 0:
            raise ValueError("Height is not achievable with given conditions")
        
        initial_velocity = math.sqrt(initial_velocity_squared)
        
        return initial_velocity
