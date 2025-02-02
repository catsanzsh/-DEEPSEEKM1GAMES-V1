import pygame
import random
import time
import numpy as np

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Game settings
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game variables
snake_block = 20
snake_speed = 15

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

# Sound generation function
def generate_beep(frequency=440, duration=0.1):
    sample_rate = 44100
    samples = np.arange(int(duration * sample_rate))
    wave = np.sin(2 * np.pi * frequency * samples / sample_rate)
    wave = np.round(wave * 32767).astype(np.int16)  # Convert to 16-bit signed integers
    sound = pygame.mixer.Sound(wave)
    return sound

# Create game sounds
eat_sound = generate_beep(880, 0.1)     # High-pitched beep for eating
game_over_sound = generate_beep(220, 0.5)  # Low-pitched beep for game over

def display_score(score):
    text = font.render("Score: " + str(score), True, WHITE)
    window.blit(text, [0, 0])

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(window, GREEN, [x[0], x[1], snake_block, snake_block])

def game_loop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
    food_y = round(random.randrange(0, height - snake_block) / snake_block) * snake_block

    while not game_over:
        while game_close:
            window.fill(BLACK)
            text = font.render("Game Over! Press Q-Quit or C-Play Again", True, WHITE)
            window.blit(text, [width/6, height/3])
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_over_sound.play()
            game_close = True

        x1 += x1_change
        y1 += y1_change
        window.fill(BLACK)
        pygame.draw.rect(window, RED, [food_x, food_y, snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over_sound.play()
                game_close = True

        draw_snake(snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            eat_sound.play()
            food_x = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
            food_y = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run the game
game_loop()
