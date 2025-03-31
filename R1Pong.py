# test.py
import tkinter as tk
from tkinter import messagebox
import threading
import pygame
import numpy as np
import random

# -------------------------------
# SOUND GENERATION
# -------------------------------
def generate_square_wave(frequency=440, duration=0.1, sample_rate=44100, amplitude=0.5):
    """Generates a square wave sound with error handling"""
    try:
        num_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, num_samples, endpoint=False)
        wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
        wave_int16 = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave_int16, wave_int16))
        return pygame.sndarray.make_sound(stereo_wave)
    except Exception as e:
        print(f"Sound generation error: {e}")
        return None

# -------------------------------
# PONG GAME USING PYGAME
# -------------------------------
def run_pong(launcher):
    """Main game function with AI opponent and improved game logic"""
    try:
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
    except Exception as e:
        messagebox.showerror("Error", f"Initialization failed: {str(e)}")
        launcher.root.deiconify()
        return

    # Game configuration
    WIDTH, HEIGHT = 600, 400
    paddle_width, paddle_height = 10, 60
    ball_radius = 8
    paddle_speed = 6
    initial_ball_speed = 5
    ai_error_margin = 0.85  # AI difficulty (1.0 = perfect)
    winning_score = 5

    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong AI Edition")
    except pygame.error as e:
        messagebox.showerror("Error", f"Display failed: {str(e)}")
        launcher.root.deiconify()
        return

    # Game state
    paddle1 = pygame.Rect(20, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)
    paddle2 = pygame.Rect(WIDTH-30, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)
    ball_pos = [WIDTH//2, HEIGHT//2]
    ball_speed = [initial_ball_speed, initial_ball_speed]
    scores = [0, 0]
    game_over = False
    winner = ""

    # Sound effects
    hit_sound = generate_square_wave(440, 0.05)
    score_sound = generate_square_wave(880, 0.2)
    wall_sound = generate_square_wave(220, 0.05)

    clock = pygame.time.Clock()
    running = True

    def reset_ball(scorer):
        """Reset ball position and speed with random angle"""
        nonlocal ball_speed
        ball_pos[:] = [WIDTH//2, HEIGHT//2]
        base_speed = initial_ball_speed * (1.1 ** sum(scores))  # Progressive difficulty
        ball_speed = [
            base_speed * (-1 if scorer else 1),
            base_speed * random.choice([-0.8, -0.6, 0.6, 0.8])
        ]

    # Main game loop
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_y:
                    # Reset game state
                    scores = [0, 0]
                    paddle1.y = HEIGHT//2 - paddle_height//2
                    paddle2.y = HEIGHT//2 - paddle_height//2
                    reset_ball(0)
                    game_over = False
                elif event.key == pygame.K_n:
                    running = False

        if not game_over:
            # Player 1 controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and paddle1.top > 0: paddle1.y -= paddle_speed
            if keys[pygame.K_s] and paddle1.bottom < HEIGHT: paddle1.y += paddle_speed

            # AI controls for Player 2
            if ball_speed[0] > 0:  # Only move when ball is approaching
                target_y = ball_pos[1] * ai_error_margin + (paddle2.centery * (1 - ai_error_margin))
                if paddle2.centery < target_y and paddle2.bottom < HEIGHT:
                    paddle2.y += paddle_speed * 0.9
                elif paddle2.centery > target_y and paddle2.top > 0:
                    paddle2.y -= paddle_speed * 0.9

            # Ball movement
            ball_pos[0] += ball_speed[0]
            ball_pos[1] += ball_speed[1]

            # Wall collisions
            if ball_pos[1] <= ball_radius or ball_pos[1] >= HEIGHT - ball_radius:
                ball_speed[1] *= -1
                if wall_sound: wall_sound.play()

            # Paddle collisions
            ball_rect = pygame.Rect(ball_pos[0]-ball_radius, ball_pos[1]-ball_radius, 
                                  ball_radius*2, ball_radius*2)
            for paddle in [paddle1, paddle2]:
                if ball_rect.colliderect(paddle):
                    ball_speed[0] *= -1
                    offset = (ball_pos[1] - paddle.centery) * 0.25
                    ball_speed[1] += offset
                    if hit_sound: hit_sound.play()
                    break

            # Scoring
            if ball_pos[0] < 0 or ball_pos[0] > WIDTH:
                scorer = 0 if ball_pos[0] > WIDTH else 1
                scores[scorer] += 1
                if score_sound: score_sound.play()
                reset_ball(scorer)
                paddle1.y = paddle2.y = HEIGHT//2 - paddle_height//2

                # Check win condition
                if scores[0] >= winning_score or scores[1] >= winning_score:
                    game_over = True
                    winner = "Player" if scores[0] >= winning_score else "AI"

        # Rendering
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), paddle1)
        pygame.draw.rect(screen, (255, 255, 255), paddle2)
        pygame.draw.circle(screen, (255, 255, 255), ball_pos, ball_radius)
        pygame.draw.aaline(screen, (128, 128, 128), (WIDTH//2, 0), (WIDTH//2, HEIGHT))

        # Score display
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"{scores[0]}   {scores[1]}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

        # Game over display
        if game_over:
            large_font = pygame.font.Font(None, 72)
            win_text = large_font.render(f"{winner} Wins!", True, (255, 255, 255))
            screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 50))
            
            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render("Restart? Y/N", True, (255, 255, 255))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    launcher.root.deiconify()

# -------------------------------
# SELF-RECURSIVE LAUNCHER
# -------------------------------
class GameLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pong Launcher")
        self.root.geometry("300x150")
        self.root.protocol("WM_DELETE_WINDOW", self.clean_exit)
        self.game_thread = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Pong AI Edition", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(self.root, text="New Game", command=self.start_game).pack(pady=5)
        tk.Button(self.root, text="Instructions", command=self.show_instructions).pack(pady=5)

    def start_game(self):
        """Start a new game thread"""
        if self.game_thread and self.game_thread.is_alive():
            return
        self.game_thread = threading.Thread(target=lambda: run_pong(self), daemon=True)
        self.game_thread.start()
        self.root.withdraw()

    def show_instructions(self):
        messagebox.showinfo("How to Play",
            "Player Controls:\n"
            "W/S - Move left paddle\n\n"
            "AI Controls:\n"
            "Right paddle auto-plays\n\n"
            "Game Rules:\n"
            "First to 5 points wins!\n"
            "ESC - Exit game")

    def clean_exit(self):
        """Proper cleanup procedure"""
        self.root.destroy()

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.root.mainloop()
