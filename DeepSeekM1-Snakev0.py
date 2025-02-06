import pygame
import random
from sys import exit

# Initialize Pygame
pygame.init()

# Set up the window dimensions
window_width = 800
window_height = 600

# Create the window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# Initialize snake, direction, and food positions
snake_pos = [(100, 100), (90, 100), (80, 100)]
direction = 'right'
food_pos = (random.randrange(1, window_width // 10) * 10, random.randrange(1, window_height // 10) * 10)

clock = pygame.time.Clock()

# Set up the game loop
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Avoid reversing direction
            if event.key == pygame.K_UP and direction != 'down':
                direction = 'up'
            elif event.key == pygame.K_DOWN and direction != 'up':
                direction = 'down'
            elif event.key == pygame.K_LEFT and direction != 'right':
                direction = 'left'
            elif event.key == pygame.K_RIGHT and direction != 'left':
                direction = 'right'

    # Move the snake: determine new head position based on current direction
    head_x, head_y = snake_pos[0]
    if direction == 'up':
        new_head = (head_x, head_y - 10)
    elif direction == 'down':
        new_head = (head_x, head_y + 10)
    elif direction == 'left':
        new_head = (head_x - 10, head_y)
    elif direction == 'right':
        new_head = (head_x + 10, head_y)

    # Check for collision with walls
    if new_head[0] < 0 or new_head[0] >= window_width or new_head[1] < 0 or new_head[1] >= window_height:
        running = False

    # Check for collision with self
    if new_head in snake_pos:
        running = False

    # Insert the new head position
    snake_pos.insert(0, new_head)

    # Check if food is eaten; if so, generate new food, else remove the tail
    if new_head == food_pos:
        food_pos = (random.randrange(1, window_width // 10) * 10, random.randrange(1, window_height // 10) * 10)
    else:
        snake_pos.pop()

    # Clear the screen
    window.fill(BLACK)

    # Draw the snake
    for pos in snake_pos:
        pygame.draw.rect(window, WHITE, (pos[0], pos[1], 10, 10))
    
    # Draw the food
    pygame.draw.rect(window, RED, (food_pos[0], food_pos[1], 10, 10))

    # Update the display and control the frame rate
    pygame.display.update()
    clock.tick(15)

# Terminate the game loop
pygame.quit()
exit()
