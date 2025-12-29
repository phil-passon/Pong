import pygame
import random
from constants import *

paddle_1_rect = PADDLE_1_START.copy()
paddle_2_rect = PADDLE_2_START.copy()
ball_rect = BALL_START_RECT.copy()

paddle_speed = 7
ball_accel_x = random.choice([-4, 4])
ball_accel_y = random.choice([-4, 4])
player1_score = 0
player2_score = 0


def reset_game():
    global player1_score, player2_score, ball_accel_x, ball_accel_y
    player1_score, player2_score = 0, 0
    paddle_1_rect.height, paddle_2_rect.height = 100, 100
    ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_accel_x, ball_accel_y = random.choice([-4, 4]), random.choice([-4, 4])


def draw_ui(screen, game_font, info_font, game_active, paused, game_over):
    # Center Line
    line_surf = pygame.Surface((4, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(line_surf, (255, 255, 255, 60), (0, y, 4, 20))
    screen.blit(line_surf, (SCREEN_WIDTH // 2 - 2, 0))

    # Score
    score_surf = game_font.render(f"{player1_score}   {player2_score}", True, COLOR_WHITE)
    screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, 50)))

    # Overlays
    if game_over:
        msg = "Player 1 Wins!" if player1_score >= WINNING_SCORE else "Player 2 Wins!"
        win_surf = game_font.render(msg, True, COLOR_WHITE)
        screen.blit(win_surf, win_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        r_text = info_font.render("Press R to Restart or ESC to Exit", True, COLOR_WHITE)
        screen.blit(r_text, r_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)))
    elif not game_active:
        txt = info_font.render("Press SPACE to Start", True, COLOR_WHITE)
        screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))
    elif paused:
        txt = info_font.render("PAUSED - Press P to Resume", True, COLOR_WHITE)
        screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))


def main():
    global ball_accel_x, ball_accel_y, player1_score, player2_score
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Load Assets from folders
    bounce_snd = pygame.mixer.Sound('sounds/bounce.wav')
    score_snd = pygame.mixer.Sound('sounds/+point.wav')
    win_snd = pygame.mixer.Sound('sounds/win sound.wav')
    game_font = pygame.font.SysFont("Consolas", 60)
    info_font = pygame.font.SysFont("Consolas", 30)

    running, game_over, game_active, paused = True, False, False, False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_ESCAPE: running = False
                    if event.key == pygame.K_r:
                        reset_game()
                        game_over, game_active = False, False
                elif not game_active:
                    if event.key == pygame.K_SPACE: game_active = True
                else:
                    if event.key == pygame.K_p: paused = not paused

        if game_active and not game_over and not paused:
            # Movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and paddle_1_rect.top > 0: paddle_1_rect.y -= paddle_speed
            if keys[pygame.K_s] and paddle_1_rect.bottom < SCREEN_HEIGHT: paddle_1_rect.y += paddle_speed
            if keys[pygame.K_UP] and paddle_2_rect.top > 0: paddle_2_rect.y -= paddle_speed
            if keys[pygame.K_DOWN] and paddle_2_rect.bottom < SCREEN_HEIGHT: paddle_2_rect.y += paddle_speed

            ball_rect.x += ball_accel_x
            ball_rect.y += ball_accel_y

            # Logic
            if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
                ball_accel_y *= -1
                bounce_snd.play()

            if ball_rect.colliderect(paddle_1_rect) or ball_rect.colliderect(paddle_2_rect):
                ball_accel_x *= -1.1
                bounce_snd.play()
                p = paddle_1_rect if ball_rect.colliderect(paddle_1_rect) else paddle_2_rect
                ball_accel_y += ((ball_rect.centery - p.centery) / (p.height / 2)) * 5

            # Scoring
            if ball_rect.left <= 0 or ball_rect.right >= SCREEN_WIDTH:
                if ball_rect.left <= 0:
                    player2_score += 1
                    if paddle_2_rect.height > 40: paddle_2_rect.height -= 10
                else:
                    player1_score += 1
                    if paddle_1_rect.height > 40: paddle_1_rect.height -= 10

                if player1_score >= WINNING_SCORE or player2_score >= WINNING_SCORE:
                    game_over = True
                    win_snd.play()
                else:
                    score_snd.play()

                ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                ball_accel_x, ball_accel_y = random.choice([-4, 4]), random.choice([-4, 4])

        # Drawing
        screen.fill(COLOR_BLACK)
        draw_ui(screen, game_font, info_font, game_active, paused, game_over)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)
        if not game_over: pygame.draw.rect(screen, COLOR_WHITE, ball_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()