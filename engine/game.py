import pygame
from player import Player
from physics import Simulation
from platforms import BasePlatform

class RunningGame:
    def __init__(self, window):
        self.is_running = False
        self.window = window
        # Setting up the fps
        self.fps = 60

    def start_game(self):
        if self.is_running:
            print("The game is already running.")
        else:
            self.is_running = True
            # Load the player image
            player_texture = pygame.image.load('engine/textures/player.png')

            # Clock font
            self.font = pygame.font.SysFont("Arial" , 18 , bold = True)

            # Creating the pymunk space
            self.sim = Simulation(self.window, self.fps, self.font)

            # Create a player object 
            self.player = Player(250, 200, player_texture, self.window, self.sim)

            # Create a platform object
            self.starting_platform = BasePlatform((200, 50), (300, 50), self.sim, self.window)
            self.test_platform = BasePlatform((300, 200), (400, 200), self.sim, self.window)

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
            self.starting_platform.draw()
            self.test_platform.draw()
            self.window.blit(self.score_string,(200,0))

            # Update the simulation
            self.sim.step()
            self.sim.fps_counter()
            self.update_score()

    def stop_game(self):
        if not self.is_running:
            print("The game is not running.")
        else:
            self.is_running = False
            print("The game has stopped.")

    def update_score(self):
        current_score = int(self.player.get_position()[1])
        if current_score > self.score + self.score_offset:
            tmp = str(current_score - self.score_offset)
            self.score_string = self.font.render(tmp, True, pygame.Color("RED"))
            self.score = current_score - self.score_offset
