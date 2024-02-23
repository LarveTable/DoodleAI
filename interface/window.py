import pygame
import random

# Initialize Pygame TURTLE JUMP
pygame.init()

# Set the width and height of the window
width = 800
height = 600

# Create the window
window = pygame.display.set_mode((width, height))

# Load a simple background image
background = pygame.image.load('interface/textures/background.png')

# Downscale the image
scaled_image = pygame.transform.scale(background, (width, height))

# Load the image for the icon
icon = pygame.image.load('interface/textures/icon.png')

# Set the icon for the window
pygame.display.set_icon(icon)

# Draw the background image
window.blit(scaled_image, (0, 0))

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the game logic here

    # Clear the window
    window.fill((0, 0, 0))
            
    # Draw the background image
    window.blit(scaled_image, (0, 0))

    # Draw game elements here

    # Update the window
    pygame.display.flip()

# Quit Pygame
pygame.quit()