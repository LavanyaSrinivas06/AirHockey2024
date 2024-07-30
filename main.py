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
    text = font.render(
        f"Player {winner} Wins! Score: {score1 if winner == 1 else score2}",
        True,
        (255, 255, 255),
    )
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


def setup():
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
    return screen, puck, paddle1, paddle2, background, clock, font


def handle_events(puck):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and not puck.started:
            puck.start()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            return False
    return True


def handle_paddle_controls(keys, paddle1, paddle2, puck_started):
    if puck_started:
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


def update_game(paddle1, paddle2, puck, puck_moving):
    puck.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    if puck.check_collision_with_paddle(paddle1) or puck.check_collision_with_paddle(
        paddle2
    ):
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
    return puck_moving


def check_goal(puck, score1, score2, puck_moving, games_played, paddle1, paddle2):
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
    return score1, score2, puck_moving, games_played


def draw(screen, background, puck, paddle1, paddle2, score1, score2, font):
    background.update()
    background.draw(screen)
    puck.draw(screen)
    paddle1.draw(screen)
    paddle2.draw(screen)
    display_scores(screen, score1, score2, font)
    pygame.display.flip()


def main():
    screen, puck, paddle1, paddle2, background, clock, font = setup()
    score1 = score2 = games_played = 0
    running = puck_moving = True
    puck_started = False

    while running and games_played < 5:
        running = handle_events(puck)
        keys = pygame.key.get_pressed()
        handle_paddle_controls(keys, paddle1, paddle2, puck.started)
        puck_moving = update_game(paddle1, paddle2, puck, puck_moving)
        score1, score2, puck_moving, games_played = check_goal(
            puck, score1, score2, puck_moving, games_played, paddle1, paddle2
        )
        draw(screen, background, puck, paddle1, paddle2, score1, score2, font)
        clock.tick(60)

    if score1 != score2:
        display_winner(screen, 1 if score1 > score2 else 2, score1, score2)
    else:
        display_game_ended(screen)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
