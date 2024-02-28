import pygame
from game import RunningGame

# Initialize Pygame TURTLE JUMP
pygame.init()

# Set the width and height of the window
width = 500
height = 800

# Create the window
window = pygame.display.set_mode((width, height))

# Load a simple background image
background = pygame.image.load('engine/textures/background.png')

# Downscale the image
scaled_image = pygame.transform.scale(background, (width, height))

# Load the image for the icon
icon = pygame.image.load('engine/textures/icon.png')

# Set the icon for the window
pygame.display.set_icon(icon)

# Draw the background image
window.blit(scaled_image, (0, 0))

# Start the game
game = RunningGame(window)
game.start_game()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the window
    window.fill((0, 0, 0))
    window.blit(scaled_image, (0, 0))

    game.run()

    pygame.display.update() # Always at the end

# Quit Pygame
pygame.quit()