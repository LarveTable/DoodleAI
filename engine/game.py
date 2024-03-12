import pygame
from player import Player
from physics import Simulation
from platforms import BasePlatform
from collections import deque
import random

class RunningGame:
    def __init__(self, window, main):
        self.is_running = False
        self.window = window
        self.main = main

        self.velocity_at_zero = 900

        self.max_platforms = 20

        # Setting up the fps
        self.fps = 60

        # Load the player image
        self.player_texture = pygame.image.load('engine/textures/player.png')

        self.displayed_platforms = deque()

        self.base_height = 400

        self.clock = pygame.time.Clock()

    def start_game(self):
        if self.is_running:
            print("The game is already running.")
        else:
            self.is_running = True

            # Clock font
            self.font = pygame.font.SysFont("Arial" , 18 , bold = True)

            # Creating the pymunk space
            self.sim = Simulation(self.window, self.fps, self.font, self.clock)

            # Create a player object 
            self.player = Player(250, 400, self.player_texture, self.window, self.sim, self)

            # Create the base platforms
            self.gen_platform()

            # Score
            self.score_offset = 315
            self.score = 0
            self.score_string = self.font.render('0', True, pygame.Color("RED"))

            print("The game has started.")

    def run(self):
        if self.is_running:
            # Draw game elements here
            self.player.draw()
            self.player.handle_input()

            # Draw the platforms
            for platform in self.displayed_platforms:
                platform.draw()

            # Draw the score
            self.window.blit(self.score_string,(200,0))

            # To DELETE
            temp_pos_str = str(int(self.player.get_position()[1]))
            temp_pos = self.font.render(temp_pos_str, True, pygame.Color("RED"))
            self.window.blit(temp_pos,(400,0))

            # Update the simulation
            self.sim.step()
            self.fps_counter()

            if self.player.get_position()[1] < 0:
                self.stop_game()

    def stop_game(self):
        if not self.is_running:
            print("The game is not running.")
        else:
            self.is_running = False
            self.sim.kill()
            print("Game over.")
            self.main.restart()
    
    def fps_counter(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps, True, pygame.Color("RED"))
        self.window.blit(fps_t,(0,0))

    def update_score(self, difference):
        self.score = self.score + difference
        self.score_string = self.font.render(str(int(self.score)), True, pygame.Color("RED"))
    
    def update_displayed_platforms(self, player_veloctiy, theoritical_height):
        if (theoritical_height >= 400):
            difference = theoritical_height - self.base_height
            if player_veloctiy < self.velocity_at_zero:
                for platform in list(self.displayed_platforms):
                    platform.move(platform.p1[1] - difference)
                    if platform.p1[1] < 0:
                        self.displayed_platforms.popleft()
                        platform.kill()
            self.update_score(difference)
        #self.gen_platform()

            
    def gen_platform(self): # A travailler mais pas mal
        while len(self.displayed_platforms) < self.max_platforms:
            if len(self.displayed_platforms) == 0:
                random_x = random.randint(10, 330)
                random_y = random.randint(20, 100)
                first = BasePlatform((random_x, random_y), (random_x+80, random_y), self.sim, self.window)
                self.displayed_platforms.append(first)

            # Get the highest platform
            highest_platform = self.displayed_platforms[-1]
            highest_platform_height = int(highest_platform.p1[1])
            print(highest_platform_height)

            random_y = random.randint(50, 250) + highest_platform_height
            random_x = random.randint(10, 330)

            print(random_x, random_y)

            # Generate a new platform
            new_platform = BasePlatform((random_x, random_y), (random_x+80, random_y), self.sim, self.window)
            self.displayed_platforms.append(new_platform)
