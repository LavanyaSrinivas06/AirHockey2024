import pygame
import sys
#from puck import Puck
from paddle import Paddle
from background import Background
import config

# Initialize Pygame
pygame.init()

def main():
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Air Hockey Game")
    
    puck = Puck(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2, config.PUCK_RADIUS, config.PUCK_COLOR, config.PUCK_INITIAL_SPEED)
    paddle1 = Paddle(10, (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) // 2, config.PADDLE_WIDTH, config.PADDLE_HEIGHT, config.PADDLE_COLOR_1, config.PADDLE_SPEED)
    paddle2 = Paddle(config.SCREEN_WIDTH - config.PADDLE_WIDTH - 10, (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) // 2, config.PADDLE_WIDTH, config.PADDLE_HEIGHT, config.PADDLE_COLOR_2, config.PADDLE_SPEED)
    background = Background(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    
    clock = pygame.time.Clock()
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
        
        background.update()
        puck.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        puck.check_collision_with_paddle(paddle1)
        puck.check_collision_with_paddle(paddle2)
        paddle1.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        paddle2.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        
        background.draw(screen)
        puck.draw(screen)
        paddle1.draw(screen)
        paddle2.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
