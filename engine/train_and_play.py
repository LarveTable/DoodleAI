import pygame
from game import RunningGame
from ai import AInstance
import main
import threading
import time

class Window:
    def __init__(self):
        # Initialize Pygame TURTLE JUMP
        pygame.init()

        # Set the width and height of the window
        width = 500
        height = 800

        # Create the window
        self.window = pygame.display.set_mode((width, height))

        # Load a simple background image
        background = pygame.image.load('engine/textures/background.png')

        # Downscale the image
        self.scaled_image = pygame.transform.scale(background, (width, height))

        # Load the image for the icon
        icon = pygame.image.load('engine/textures/icon.png')

        # Set the icon for the window
        pygame.display.set_icon(icon)

        # Draw the background image
        self.window.blit(self.scaled_image, (0, 0))

        self.player_count = 1

        self.games_stopped = 0

        self.results = {}

        self.generation = 0

        self.max_generation = 10

        self.force_exit = False

    # Start the game
    def start_game(self, player, generation, barrier):
        ai = AInstance(generation, player)
        game = RunningGame(self.window, self, ai, self.player_count)
        game.start_game()
        self.update_game(game, barrier)

    def update_game(self, game, barrier):
        while game.is_running:
            game.run()
            barrier.wait()
        del game
        while self.running:
            barrier.wait()

    def refresh(self, barrier):
        # Game loop
        self.running = True

        while self.running:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.force_exit = True
                    barrier.abort()
                    break

            # Clear the window
            self.window.fill((0, 0, 0))
            self.window.blit(self.scaled_image, (0, 0))

            if (self.games_stopped == self.player_count):
                self.running = False
                print("All games have stopped.")
                best_key = max(self.results.keys())
                best_value = self.results[best_key]
                print("Best player : " + str(int(best_value[0])) + " with a score of " + str(best_key) + " and weights : " + str(best_value[1]))
                self.generation += 1

            barrier.wait()

            pygame.display.update() # Always at the end

        if (self.generation > self.max_generation and not self.force_exit):
            print("Training finished with a max score of : " + str(best_key) + " and weights : " + str(best_value[1]))
            # Quit Pygame
            pygame.quit()
        elif (not self.force_exit):
            self.games_stopped = 0
            self.results = {}
            barrier = trainings(self, best_value[1])
            self.refresh(barrier)

# Create the window
window = Window()

def trainings(window, weights):
    print("Generation "+str(window.generation)+", training with weights : " + str(weights))
    threads = []
    barrier = threading.Barrier(window.player_count+1)
    generation = main.AIGeneration(window.player_count, weights)
    generation.mutatePlayers()
    for p in generation.players:
        thread = threading.Thread(target=window.start_game, args=(p, generation, barrier))
        threads.append(thread)

    for t in threads:
        t.start()
    
    return barrier

barrier = trainings(window, [-1, 1.7, 2.6])
window.refresh(barrier)