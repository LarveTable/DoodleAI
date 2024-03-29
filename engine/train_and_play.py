import pygame
from game import RunningGame
from ai import AInstance

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

        self.nbTrials = 0

    # Start the game
    def start_game(self):
        print("Trial number: ", self.nbTrials)
        self.game = RunningGame(self.window, self)
        self.game.start_game()

    def run(self):

        self.start_game()

        self.ai = AInstance(self.game)

        # Game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the window
            self.window.fill((0, 0, 0))
            self.window.blit(self.scaled_image, (0, 0))

            self.game.run()

            pygame.display.update() # Always at the end

        # Quit Pygame
        pygame.quit()

    def restart(self):
        del self.game
        self.nbTrials += 1
        self.start_game()

# Create the window
window = Window()
window.run()