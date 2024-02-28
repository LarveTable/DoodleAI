import pygame
from player import Player
from physics import Simulation
from platforms import BasePlatform
from collections import deque

class RunningGame:
    def __init__(self, window):
        self.is_running = False
        self.window = window


        self.max_platforms = 20

        # Setting up the fps
        self.fps = 60

        # Load the player image
        self.player_texture = pygame.image.load('engine/textures/player.png')

        self.displayed_platforms = deque()

        self.previous_move = 400

    def start_game(self):
        if self.is_running:
            print("The game is already running.")
        else:
            self.is_running = True

            # Clock font
            self.font = pygame.font.SysFont("Arial" , 18 , bold = True)

            # Creating the pymunk space
            self.sim = Simulation(self.window, self.fps, self.font)

            # Create a player object 
            self.player = Player(250, 200, self.player_texture, self.window, self.sim)

            # Create the base platform
            starting_platform = BasePlatform((200, 50), (300, 50), self.sim, self.window)
            test = BasePlatform((350, 200), (450, 200), self.sim, self.window)
            test2 = BasePlatform((100, 400), (200, 400), self.sim, self.window)
            self.displayed_platforms.append(starting_platform)
            self.displayed_platforms.append(test2)
            self.displayed_platforms.append(test)

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
            self.window.blit(self.score_string,(200,0))

            # Update the simulation
            self.sim.step()
            self.sim.fps_counter()
            self.update_score()
            self.update_displayed_platforms()

            if self.player.get_position()[1] < 0:
                self.stop_game()

    def stop_game(self):
        if not self.is_running:
            print("The game is not running.")
        else:
            self.is_running = False
            print("Game over.")

    def update_score(self):
        current_score = int(self.player.get_position()[1])
        if current_score > self.score + self.score_offset:
            tmp = str(current_score - self.score_offset)
            self.score_string = self.font.render(tmp, True, pygame.Color("RED"))
            self.score = current_score - self.score_offset

    def get_displayed_platforms(self):
        return self.displayed_platforms
    
    def update_displayed_platforms(self):
        snap = self.player.get_position()[1]
        if snap > 400 and snap > self.previous_move:
            for p in self.displayed_platforms:
                p.move(p.p1[1]-(snap - self.previous_move))
            self.previous_move = snap
    
    def gen_platform(self):
        if len(self.displayed_platforms) < self.max_platforms:
            pass
