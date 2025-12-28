import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
WINNING_SCORE = 10

# --- Global Objects ---
paddle_1_rect = pygame.Rect(30, SCREEN_HEIGHT // 2 - 50, 7, 100)
paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, 7, 100)
ball_rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 25, 25)

# Game State Variables
paddle_speed = 7
ball_accel_x = random.choice([-4, 4])
ball_accel_y = random.choice([-4, 4])
player1_score = 0
player2_score = 0


def reset_game():
    global player1_score, player2_score, ball_accel_x, ball_accel_y
    player1_score = 0
    player2_score = 0
    ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_accel_x = random.choice([-4, 4])
    ball_accel_y = random.choice([-4, 4])


def draw_center_line(screen):
    line_surface = pygame.Surface((4, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(line_surface, (255, 255, 255, 60), (0, y, 4, 20))
    screen.blit(line_surface, (SCREEN_WIDTH // 2 - 2, 0))


def draw_score(screen, font):
    score_text = f"{player1_score}   {player2_score}"
    score_surface = font.render(score_text, True, COLOR_WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)


def main():
    global ball_accel_x, ball_accel_y, player1_score, player2_score
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    # Load Assets
    bounce_sound = pygame.mixer.Sound('bounce.wav')
    score_sound = pygame.mixer.Sound('+point.wav')
    win_sound = pygame.mixer.Sound('win sound.wav')
    game_font = pygame.font.SysFont("Consolas", 60)
    info_font = pygame.font.SysFont("Consolas", 30)

    running = True
    game_over = False
    game_active = False
    paused = False  # New state variable for pausing

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Toggle Pause with 'P'
            if game_active and not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

            # Start Screen Controls
            if not game_active and not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True

            # Win Screen Controls
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    reset_game()
                    game_over = False
                    game_active = False

        # Only update physics if active and NOT paused
        if game_active and not game_over and not paused:
            # Paddle Movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and paddle_1_rect.top > 0: paddle_1_rect.y -= paddle_speed
            if keys[pygame.K_s] and paddle_1_rect.bottom < SCREEN_HEIGHT: paddle_1_rect.y += paddle_speed
            if keys[pygame.K_UP] and paddle_2_rect.top > 0: paddle_2_rect.y -= paddle_speed
            if keys[pygame.K_DOWN] and paddle_2_rect.bottom < SCREEN_HEIGHT: paddle_2_rect.y += paddle_speed

            # Ball Physics
            ball_rect.x += ball_accel_x
            ball_rect.y += ball_accel_y

            if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
                ball_accel_y *= -1

            if ball_rect.colliderect(paddle_1_rect) or ball_rect.colliderect(paddle_2_rect):
                ball_accel_x *= -1.1
                ball_accel_y *= 1.1
                bounce_sound.play()

            # Scoring Logic
            if ball_rect.left <= 0:
                player2_score += 1
                if player2_score < WINNING_SCORE: score_sound.play()
                ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                ball_accel_x, ball_accel_y = random.choice([-4, 4]), random.choice([-4, 4])
                game_active = False

            if ball_rect.right >= SCREEN_WIDTH:
                player1_score += 1
                if player1_score < WINNING_SCORE: score_sound.play()
                ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                ball_accel_x, ball_accel_y = random.choice([-4, 4]), random.choice([-4, 4])
                game_active = False

            if player1_score >= WINNING_SCORE or player2_score >= WINNING_SCORE:
                game_over = True
                win_sound.play()

        # --- Drawing ---
        screen.fill(COLOR_BLACK)
        draw_center_line(screen)
        draw_score(screen, font=game_font)

        # Draw Paddles
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)

        if not game_over:
            pygame.draw.rect(screen, COLOR_WHITE, ball_rect)

            # Draw UI messages based on state
            if not game_active:
                start_surf = info_font.render("Press SPACE to Start", True, COLOR_WHITE)
                screen.blit(start_surf, start_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))
            elif paused:
                pause_surf = info_font.render("PAUSED - Press P to Resume", True, COLOR_WHITE)
                screen.blit(pause_surf, pause_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        else:
            # Win UI
            msg = "Player 1 Wins!" if player1_score >= WINNING_SCORE else "Player 2 Wins!"
            win_surf = game_font.render(msg, True, COLOR_WHITE)
            screen.blit(win_surf, win_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

            esc_surf = info_font.render("Press ESCAPE to Exit", True, COLOR_WHITE)
            screen.blit(esc_surf, esc_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))

            r_surf = info_font.render("Press R to Restart", True, COLOR_WHITE)
            screen.blit(r_surf, r_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()