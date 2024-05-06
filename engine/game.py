import pygame
from player import Player
from physics import Simulation
from platforms import BasePlatform
from collections import deque
import random
import main

class RunningGame:
    def __init__(self, window, main, ai, player_count):
        self.is_running = False
        self.window = window
        self.main = main
        self.ai = ai
        self.player_count = player_count

        self.platform_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
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
            self.player = Player(250, 0, self.player_texture, self.window, self.sim, self)

            # Create the base platforms
            self.gen_platform()

            # Score
            self.score = 0
            self.score_string = self.font.render('Score : 0', True, pygame.Color("RED"))

            #print("The game has started for player : "+str(self.ai.player.identifier)+".")

    def run(self):
        if self.is_running:

            if self.player_count > 1:
                self.player.draw()

                # Update the simulation
                self.sim.step()

                self.ai.update_state(self)
                self.player.move(x=self.player.get_position()[0]+self.ai.make_move(), y=self.player.get_position()[1])

                if self.player.get_position()[1] < 0:
                    self.stop_game()

            else:
                # Draw game elements here
                self.player.draw()
                self.player.handle_input()

                # Draw the score
                self.window.blit(self.score_string,(300,0))

                # Draw the platforms
                for platform in self.displayed_platforms:
                    platform.draw()

                # Update the simulation
                self.sim.step()
                self.fps_counter()

                self.ai.update_state(self)
                move = self.ai.make_move()
                nearest = self.ai.get_nearest_platform()
                move_string = self.font.render("move : "+str(move), True, pygame.Color("GREEN"))
                for platform in self.displayed_platforms: #check if nearest if valid
                    if platform.body.id == nearest:
                        #change color of the platform
                        platform.color = (255, 0, 0)
                self.window.blit(move_string,(200,400))
                self.player.move(x=self.player.get_position()[0]+move, y=self.player.get_position()[1])

                if self.player.get_position()[1] < 0:
                    self.stop_game()

    def get_state(self):
        state = main.State()
        state.playerPos = [self.player.get_position()[0], self.player.get_position()[1]]
        state.playerVel = self.player.body.velocity[1]
        plats = []
        for platform in self.displayed_platforms:
            p = main.Platform()
            p.width = platform.p2[0] - platform.p1[0]
            #x and y should be the center of the platform
            p.x = platform.p1[0] + p.width/2
            p.y = platform.p1[1]
            p.id = platform.body.id
            plats.append(p)
        state.score = int(self.score)
        state.platforms = plats

        if self.player.last_touched is None:
            last_touched = main.Platform()
            last_touched.x = 0
            last_touched.y = 0
            last_touched.width = 0
            last_touched.id = 0
        else:
            last_touched = main.Platform()
            last_touched.x = self.player.last_touched.a[0]
            last_touched.y = self.player.last_touched.a[1]
            last_touched.width = self.player.last_touched.b[0] - self.player.last_touched.a[0]
            last_touched.id = self.player.last_touched.body.id

        state.lastTouchedPlatform = last_touched
        state.touchedPlatforms = len(self.player.platforms_touched)

        return state

    def stop_game(self):
        if not self.is_running:
            print("The game is not running.")
        else:
            self.is_running = False
            self.sim.kill()
            self.main.games_stopped += 1
            self.main.results[self.ai.player.state.score] = [self.ai.player.identifier, self.ai.player.weights]
            del self.ai
    
    def fps_counter(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps, True, pygame.Color("RED"))
        self.window.blit(fps_t,(0,0))

    def update_score(self, difference):
        self.score = self.score + difference
        self.score_string = self.font.render("Score : "+str(int(self.score)), True, pygame.Color("RED"))
    
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
        self.gen_platform()

            
    def gen_platform(self): # A travailler mais pas mal
        while len(self.displayed_platforms) < self.max_platforms:
            if len(self.displayed_platforms) == 0:
                random_x = random.randint(10, 330)
                random_y = random.randint(20, 100)
                first = BasePlatform((random_x, random_y), (random_x+80, random_y), self.sim, self.window, self.platform_color)
                self.displayed_platforms.append(first)

            # Get the highest platform
            highest_platform = self.displayed_platforms[-1]
            highest_platform_height = int(highest_platform.p1[1])

            random_y = random.randint(50, 250) + highest_platform_height
            random_x = random.randint(10, 330)

            # Generate a new platform
            new_platform = BasePlatform((random_x, random_y), (random_x+80, random_y), self.sim, self.window, self.platform_color)
            self.displayed_platforms.append(new_platform)
