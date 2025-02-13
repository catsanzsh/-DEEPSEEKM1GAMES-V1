import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20
FPS = 10

# Colors
BG_COLOR = (0, 0, 0)  # Black
SNAKE_HEAD_COLOR = (220, 20, 60)  # Crimson
SNAKE_BODY_COLOR = (255, 99, 71)  # Tomato
FOOD_COLOR = (255, 215, 0)  # Gold
DECO_COLOR = (178, 34, 34)  # Firebrick
TEXT_COLOR = (255, 255, 255)  # White

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Year of the Snake 2024 - Score: 0")
clock = pygame.time.Clock()

# Snake initialization
snake = [(WIDTH//2, HEIGHT//2)]
dx, dy = CELL_SIZE, 0
score = 0

# Food initialization
food = (random.randrange(0, WIDTH, CELL_SIZE), 
        random.randrange(0, HEIGHT, CELL_SIZE))

# Font for score display
font = pygame.font.SysFont('helvetica', 30, bold=True)

def draw_lantern(x, y):
    """Draw Chinese lantern using geometric shapes"""
    # Lantern body
    pygame.draw.rect(screen, DECO_COLOR, (x, y, 40, 60))
    pygame.draw.rect(screen, (139, 0, 0), (x, y, 40, 60), 2)
    
    # Top and bottom decorations
    pygame.draw.line(screen, (255, 215, 0), (x-5, y), (x+45, y), 3)
    pygame.draw.line(screen, (255, 215, 0), (x-5, y+60), (x+45, y+60), 3)
    
    # Hanging string
    pygame.draw.line(screen, (255, 215, 0), (x+20, y-20), (x+20, y), 2)

def game_over():
    """Display game over screen"""
    screen.fill(BG_COLOR)
    text = font.render(f'Game Over! Final Score: {score}', True, TEXT_COLOR)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL_SIZE
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL_SIZE
            elif event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL_SIZE, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL_SIZE, 0

    # Move snake
    new_head = (snake[0][0] + dx, snake[0][1] + dy)
    snake.insert(0, new_head)

    # Check food collision
    if snake[0] == food:
        score += 1
        pygame.display.set_caption(f"Year of the Snake 2024 - Score: {score}")
        while True:
            new_food = (random.randrange(0, WIDTH, CELL_SIZE),
                        random.randrange(0, HEIGHT, CELL_SIZE))
            if new_food not in snake:
                food = new_food
                break
    else:
        snake.pop()

    # Collision detection
    if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
        snake[0][1] < 0 or snake[0][1] >= HEIGHT or
        snake[0] in snake[1:]):
        game_over()

    # Drawing
    screen.fill(BG_COLOR)
    
    # Draw decorative lanterns
    draw_lantern(50, 50)
    draw_lantern(WIDTH-90, 50)
    
    # Draw snake
    for i, segment in enumerate(snake):
        color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
        pygame.draw.rect(screen, color, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    
    # Draw food
    pygame.draw.circle(screen, FOOD_COLOR, 
                      (food[0] + CELL_SIZE//2, food[1] + CELL_SIZE//2),
                      CELL_SIZE//2)
    
    # Draw title text
    title_text = font.render("Year of the Snake 2024", True, TEXT_COLOR)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 10))
    
    pygame.display.flip()
    clock.tick(FPS)
