import pygame
import random

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# Initialize Objects
paddle_1_rect = pygame.Rect(30, SCREEN_HEIGHT // 2 - 50, 7, 100)
paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, 7, 100)
ball_rect = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 25, 25)

# Movement speeds
paddle_speed = 7
ball_accel_x = random.choice([-4, 4])
ball_accel_y = random.choice([-4, 4])

# Score variables
player1_score = 0
player2_score = 0


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

    # Sound variables
    bounce_sound = pygame.mixer.Sound('bounce.wav')
    score_sound = pygame.mixer.Sound('+point.wav')
    win_sound = pygame.mixer.Sound('win sound.wav')

    # Fonts:
    game_font = pygame.font.SysFont("Consolas", 60)
    info_font = pygame.font.SysFont("Consolas", 30)

    running = True
    game_over = False

    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Controls for when the game is over
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    player1_score = 0
                    player2_score = 0
                    ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    ball_accel_x = random.choice([-4, 4])
                    ball_accel_y = random.choice([-4, 4])
                    game_over = False

        if not game_over:
            # Holding the key moves the paddle
            keys = pygame.key.get_pressed()
            # Player 1 (W/S Keys)
            if keys[pygame.K_w] and paddle_1_rect.top > 0:
                paddle_1_rect.y -= paddle_speed
            if keys[pygame.K_s] and paddle_1_rect.bottom < SCREEN_HEIGHT:
                paddle_1_rect.y += paddle_speed

            # Player 2 (Up/Down Arrows)
            if keys[pygame.K_UP] and paddle_2_rect.top > 0:
                paddle_2_rect.y -= paddle_speed
            if keys[pygame.K_DOWN] and paddle_2_rect.bottom < SCREEN_HEIGHT:
                paddle_2_rect.y += paddle_speed

            # Movement & Bouncing
            ball_rect.x += ball_accel_x
            ball_rect.y += ball_accel_y

            # Wall Bouncing
            if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
                ball_accel_y *= -1

            # Paddle Bouncing
            if ball_rect.colliderect(paddle_1_rect) or ball_rect.colliderect(paddle_2_rect):
                ball_accel_x *= -1.1  # Increases speed by 10%
                ball_accel_y *= 1.1
                bounce_sound.play()

            # Scoring Logic
            if ball_rect.left <= 0:
                player2_score += 1
                ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                ball_accel_x = random.choice([-4, 4])
                ball_accel_y = random.choice([-4, 4])
                # Only play score sound if no one won yet
                if player2_score < 2:
                    score_sound.play()

            if ball_rect.right >= SCREEN_WIDTH:
                player1_score += 1
                ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                ball_accel_x = random.choice([-4, 4])
                ball_accel_y = random.choice([-4, 4])
                # Only play score sound if no one won yet
                if player1_score < 2:
                    score_sound.play()

            # Check for a winner
            if player1_score >= 10 or player2_score >= 10:
                game_over = True
                win_sound.play() # Only victory sound plays for final point

        # Drawing Logic
        screen.fill(COLOR_BLACK)

        # Translucent center line
        line_surface = pygame.Surface((4, SCREEN_HEIGHT), pygame.SRCALPHA)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.rect(line_surface, (255, 255, 255, 60), (0, y, 4, 20))
        screen.blit(line_surface, (SCREEN_WIDTH // 2 - 2, 0))

        draw_score(screen, game_font)

        # Only draw paddles and ball if the game is still going
        if not game_over:
            pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
            pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)
            pygame.draw.rect(screen, COLOR_WHITE, ball_rect)
        else:
            pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
            pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)

            # Draw Win Text
            if player1_score >= 10:
                win_text = "Player 1 Wins!"
            else:
                win_text = "Player 2 Wins!"

            win_surface = game_font.render(win_text, True, COLOR_WHITE)
            win_rect = win_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(win_surface, win_rect)

            exit_text = "Press ESCAPE to Exit"
            exit_surface = info_font.render(exit_text, True, COLOR_WHITE)
            exit_rect = exit_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(exit_surface, exit_rect)

            restart_text = "Press R to Restart"
            restart_surface = info_font.render(restart_text, True, COLOR_WHITE)
            restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            screen.blit(restart_surface, restart_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()