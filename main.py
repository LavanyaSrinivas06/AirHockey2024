import pygame
import sys
import config
from paddle import Paddle
from puck import Puck
from background import Background

# Initialize Pygame
pygame.init()
#initialize the mixer for sound
pygame.mixer.init()

# Load sound effects
paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")  # Add the path to your paddle hit sound
goal_sound = pygame.mixer.Sound("goal.wav")  # Add the path to your goal sound
#set the volume of the sound effects
paddle_hit_sound.set_volume(0.5)
goal_sound.set_volume(0.5)

def display_scores(screen, score1, score2, font):
    score_text = font.render(
        f"Player 1: {score1}  Player 2: {score2}", True, (255, 255, 255)
    )
    screen.blit(
        score_text, (config.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20)
    )

def reset_puck(puck):
    puck.x = config.SCREEN_WIDTH // 2
    puck.y = config.SCREEN_HEIGHT // 2
    puck.vx = 0
    puck.vy = 0
    puck.started = False

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
    score1 = 0
    score2 = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not puck.started:
                puck.start()

        keys = pygame.key.get_pressed()

        # Player 1 Controls
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

        # Player 2 Controls
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

        # Update game objects
        background.update()
        puck.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

        # Check for paddle collision and play sound
        if puck.check_collision_with_paddle(paddle1) or puck.check_collision_with_paddle(paddle2):
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

        # Check for scoring
        if (
            puck.x - puck.radius <= 0
            and (config.SCREEN_HEIGHT // 2) - 100
            < puck.y
            < (config.SCREEN_HEIGHT // 2) + 100
        ):
            score2 += 1
            goal_sound.play()  # Play goal sound
            puck.reset(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
        elif (
            puck.x + puck.radius >= config.SCREEN_WIDTH
            and (config.SCREEN_HEIGHT // 2) - 100
            < puck.y
            < (config.SCREEN_HEIGHT // 2) + 100
        ):
            score1 += 1
            goal_sound.play()  # Play goal sound
            puck.reset(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        # Draw everything
        background.draw(screen)
        puck.draw(screen)
        paddle1.draw(screen)
        paddle2.draw(screen)
        display_scores(screen, score1, score2, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
