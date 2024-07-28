import pygame
import config
from paddle import Paddle
from puck import Puck
from background import Background
import unittest

class AirHockeyTest(unittest.TestCase):

    def setUp(self):
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Air Hockey Game Test")
        
        # Initialize game objects
        self.puck = Puck(
            config.SCREEN_WIDTH // 2,
            config.SCREEN_HEIGHT // 2,
            config.PUCK_RADIUS,
            config.PUCK_COLOR,
            config.PUCK_INITIAL_SPEED,
        )
        self.paddle1 = Paddle(
            10,
            (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) // 2,
            config.PADDLE_WIDTH,
            config.PADDLE_HEIGHT,
            config.PADDLE_COLOR_1,
            config.PADDLE_SPEED,
        )
        self.paddle2 = Paddle(
            config.SCREEN_WIDTH - config.PADDLE_WIDTH - 10,
            (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) // 2,
            config.PADDLE_WIDTH,
            config.PADDLE_HEIGHT,
            config.PADDLE_COLOR_2,
            config.PADDLE_SPEED,
        )
        self.background = Background(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        
        # Load sound effects
        self.paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
        self.goal_sound = pygame.mixer.Sound("goal.wav")
        self.paddle_hit_sound.set_volume(0.5)
        self.goal_sound.set_volume(0.5)

    def tearDown(self):
        pygame.quit()

    def test_paddle_movement(self):
        # Simulate paddle movement
        self.paddle1.move_up()
        self.paddle1.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, config.SCREEN_WIDTH // 2)
        self.assertEqual(self.paddle1.vy, -self.paddle1.speed)
        
        self.paddle2.move_down()
        self.paddle2.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.SCREEN_WIDTH // 2, config.SCREEN_WIDTH)
        self.assertEqual(self.paddle2.vy, self.paddle2.speed)

    def test_puck_start(self):
        self.puck.start()
        self.assertTrue(self.puck.started)
        self.assertEqual(self.puck.vx, config.PUCK_INITIAL_SPEED)
        self.assertEqual(self.puck.vy, config.PUCK_INITIAL_SPEED)

    def test_paddle_collision_sound(self):
        # Position puck for collision with paddle1
        self.puck.x = self.paddle1.x + self.paddle1.width + self.puck.radius - 1
        self.puck.y = self.paddle1.y + self.paddle1.height // 2
        self.puck.vx = -self.puck.vx  # Ensure movement towards paddle
        self.puck.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        
        collision = self.puck.check_collision_with_paddle(self.paddle1)
        if collision:
            self.paddle_hit_sound.play()

        self.assertTrue(collision)

    def test_wall_collision(self):
        # Position puck for collision with wall
        self.puck.x = self.puck.radius
        self.puck.vx = -self.puck.vx
        self.puck.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        
        self.assertEqual(self.puck.vx, config.PUCK_INITIAL_SPEED)

    def test_scoring(self):
        # Simulate scoring
        self.puck.x = self.puck.radius - 1  # Near left goal
        self.puck.y = config.SCREEN_HEIGHT // 2
        score2 = 0
        if self.puck.x - self.puck.radius <= 0 and config.SCREEN_HEIGHT // 2 - 100 < self.puck.y < config.SCREEN_HEIGHT // 2 + 100:
            score2 += 1
            self.goal_sound.play()
            self.puck.reset()

        self.assertEqual(score2, 1)
        self.assertEqual(self.puck.x, config.SCREEN_WIDTH // 2)
        self.assertEqual(self.puck.y, config.SCREEN_HEIGHT // 2)

    def test_game_over(self):
        # Simulate game over scenario
        score1 = 5
        score2 = 3
        if score1 >= 5 or score2 >= 5:
            winner = 1 if score1 > score2 else 2
            self.assertEqual(winner, 1)
            # Additional logic to display winner can be tested here

if __name__ == "__main__":
    unittest.main()
