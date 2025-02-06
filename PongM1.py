# Description: Pong game with two paddles and a ball. The paddles are controlled by the player using the arrow keys and the 'W' and 'S' keys. The game ends when the ball goes out of bounds. The player with the highest score wins.
import pygame

# Initialize Pygame
pygame.init()

# Set up the display
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Paddle dimensions and positions
paddle_width = 10
paddle_height = 100

left_paddle = pygame.Rect(20, height//2 - paddle_height//2, paddle_width, paddle_height)
right_paddle = pygame.Rect(width-40, height//2 - paddle_height//2, paddle_width, paddle_height)

# Ball dimensions and initial position
ball_radius = 5
ball_x = width // 2
ball_y = height // 2

# Initial ball direction
ball_dx = 4
ball_dy = 4

# Score variables
left_score = 0
right_score = 0

# Game loop clock
clock = pygame.time.Clock()

running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                left_paddle.top = max(0, left_paddle.top - 10)
            elif event.key == pygame.K_DOWN:
                left_paddle.top = min(height - paddle_height, left_paddle.top + 10)
            elif event.key == pygame.K_w:
                right_paddle.top = max(0, right_paddle.top - 10)
            elif event.key == pygame.K_s:
                right_paddle.top = min(height - paddle_height, right_paddle.top + 10)

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Check for collisions with paddles
    if (ball_x > left_paddle.left and ball_x < left_paddle.left + paddle_width and 
        ball_y > left_paddle.top and ball_y < left_paddle.bottom):
        ball_dx = -4
    elif (ball_x > width - right_paddle.left - paddle_width and 
          ball_x < width - right_paddle.left and 
          ball_y > right_paddle.top and ball_y < right_paddle.bottom):
        ball_dx = 4

    # Ball hits top or bottom of the screen
    if ball_y < ball_radius or ball_y > height - ball_radius:
        ball_dy *= -1

    # Check for scores
    if ball_x < 0:
        left_score += 1
        ball_x = width // 2
        ball_y = height // 2
        ball_dx = 4
    elif ball_x > width:
        right_score += 1
        ball_x = width // 2
        ball_y = height // 2
        ball_dx = -4

    # Update the display
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, left_paddle)
    pygame.draw.rect(screen, RED, right_paddle)
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

    # Display scores
    font = pygame.font.Font(None, 74)
    text_left = font.render(str(left_score), True, WHITE)
    text_right = font.render(str(right_score), True, WHITE)
    screen.blit(text_left, (width//2 - 100, 50))
    screen.blit(text_right, (width//2 + 100, 50))

    # Draw net
    pygame.draw.line(screen, WHITE, (width//2, 0), (width//2, height), 2)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
# Compare this snippet from sm64.py:
