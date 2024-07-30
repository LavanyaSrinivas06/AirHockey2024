import pygame
import sys
import config
from paddle import Paddle
from puck import Puck
from background import Background


pygame.init()
pygame.mixer.init()

paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
goal_sound = pygame.mixer.Sound("goal.wav")
paddle_hit_sound.set_volume(0.5)
goal_sound.set_volume(0.5)


def display_winner(screen, winner, score1, score2):
    font = pygame.font.Font(None, 74)
    if winner == 1:
        text = font.render(f"Player 1 Wins! Score: {score1}", True, (255, 255, 255))
    else:
        text = font.render(f"Player 2 Wins! Score: {score2}", True, (255, 255, 255))
    text_rect = text.get_rect(
        center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
    )
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


def display_game_ended(screen):
    font = pygame.font.Font(None, 74)
    text = font.render("Game Ended", True, (255, 255, 255))
    text_rect = text.get_rect(
        center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
    )
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


def display_scores(screen, score1, score2, font):
    score_text = font.render(
        f"Player 1: {score1}  Player 2: {score2}", True, (255, 255, 255)
    )
    screen.blit(
        score_text, (config.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20)
    )


def reset_game(puck, paddle1, paddle2):
    puck.reset(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
    paddle1.reset()
    paddle2.reset()


def main():
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Air Hockey Game")

    puck = Puck(
        config.SCREEN_WIDTH // 2,
        config.SCREEN_HEIGHT // 2,
        config.PUCK_RADIUS,
        config.PUCK_COLOR,
        config.PUCK_INITIAL_SPEED,
    )
    paddle1 = Paddle(
        10,
        (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) // 2,
        config.PADDLE_WIDTH,
        config.PADDLE_HEIGHT,
        config.PADDLE_COLOR_1,
        config.PADDLE_SPEED,
    )
    paddle2 = Paddle(
        config.SCREEN_WIDTH - config.PADDLE_WIDTH - 10,
        (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) // 2,
        config.PADDLE_WIDTH,
        config.PADDLE_HEIGHT,
        config.PADDLE_COLOR_2,
        config.PADDLE_SPEED,
    )
    background = Background(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74)
    running = True

    score1 = 0
    score2 = 0
    games_played = 0

    puck_moving = False

    while running and games_played < 5:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not puck.started:
                puck.start()
                puck_moving = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        keys = pygame.key.get_pressed()

        if puck_moving:
            # Paddle 1 controls
            if keys[pygame.K_w]:
                paddle1.move_up()
            if keys[pygame.K_s]:
                paddle1.move_down()
            if keys[pygame.K_a]:
                paddle1.move_left()
            if keys[pygame.K_d]:
                paddle1.move_right()
            if not keys[pygame.K_w] and not keys[pygame.K_s]:
                paddle1.stop_vertical()
            if not keys[pygame.K_a] and not keys[pygame.K_d]:
                paddle1.stop_horizontal()

            # Paddle 2 controls
            if keys[pygame.K_UP]:
                paddle2.move_up()
            if keys[pygame.K_DOWN]:
                paddle2.move_down()
            if keys[pygame.K_LEFT]:
                paddle2.move_left()
            if keys[pygame.K_RIGHT]:
                paddle2.move_right()
            if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                paddle2.stop_vertical()
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                paddle2.stop_horizontal()

        background.update()
        puck.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

        if puck.check_collision_with_paddle(
            paddle1
        ) or puck.check_collision_with_paddle(paddle2):
            paddle_hit_sound.play()

        paddle1.update(
            config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, config.SCREEN_WIDTH // 2
        )
        paddle2.update(
            config.SCREEN_WIDTH,
            config.SCREEN_HEIGHT,
            config.SCREEN_WIDTH // 2,
            config.SCREEN_WIDTH,
        )

        if (
            puck.x - puck.radius <= 0
            and (config.SCREEN_HEIGHT // 2) - 100
            < puck.y
            < (config.SCREEN_HEIGHT // 2) + 100
        ):
            score2 += 1
            goal_sound.play()
            reset_game(puck, paddle1, paddle2)
            puck_moving = False
            games_played += 1
        elif (
            puck.x + puck.radius >= config.SCREEN_WIDTH
            and (config.SCREEN_HEIGHT // 2) - 100
            < puck.y
            < (config.SCREEN_HEIGHT // 2) + 100
        ):
            score1 += 1
            goal_sound.play()
            reset_game(puck, paddle1, paddle2)
            puck_moving = False
            games_played += 1

        background.draw(screen)
        puck.draw(screen)
        paddle1.draw(screen)
        paddle2.draw(screen)
        display_scores(screen, score1, score2, font)

        pygame.display.flip()
        clock.tick(60)

    if score1 > score2:
        winner = 1
    elif score2 > score1:
        winner = 2
    else:
        winner = None

    if winner is not None:
        display_winner(screen, winner, score1, score2)
    else:
        if score1 == 0 and score2 == 0:
            display_game_ended(screen)
        else:
            font = pygame.font.Font(None, 74)
            text = font.render(
                f"Game Tied! Score: {score1}-{score2}", True, (255, 255, 255)
            )
            text_rect = text.get_rect(
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
            )
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
