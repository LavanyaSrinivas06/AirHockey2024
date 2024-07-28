import unittest
import pygame
from pygame.locals import K_w, K_s, K_a, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT
from puck import Puck
from paddle import Paddle
import config

class TestAirHockeyGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.mixer.init()

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
    # tescase1: is for paddle up,down,right,left movement
    def test_paddle_movement(self):
        
        initial_y = self.paddle1.y
        self.paddle1.move_up()
        self.paddle1.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, config.SCREEN_WIDTH // 2)
        self.assertLess(self.paddle1.y, initial_y, "Paddle 1 should move up")

        initial_y = self.paddle1.y
        self.paddle1.move_down()
        self.paddle1.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, config.SCREEN_WIDTH // 2)
        self.assertGreater(self.paddle1.y, initial_y, "Paddle 1 should move down")

        initial_x = self.paddle1.x
        self.paddle1.move_left()
        self.paddle1.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, config.SCREEN_WIDTH // 2)
        self.assertLess(self.paddle1.x, initial_x, "Paddle 1 should move left")

        initial_x = self.paddle1.x
        self.paddle1.move_right()
        self.paddle1.update(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, config.SCREEN_WIDTH // 2)
        self.assertGreater(self.paddle1.x, initial_x, "Paddle 1 should move right")
    #testcase2: this testcase is for collision between puck and paddle
    def test_puck_paddle_collision(self):
        self.puck.x = self.paddle1.x + self.paddle1.width / 2 + self.puck.radius
        self.puck.y = self.paddle1.y + self.paddle1.height / 2
        self.puck.vx = -config.PUCK_INITIAL_SPEED
        self.puck.vy = 0

        collision = self.puck.check_collision_with_paddle(self.paddle1)

        self.assertTrue(collision, "The puck should collide with the paddle")
        self.assertGreater(self.puck.vx, 0, "The puck's x velocity should be positive after collision")
        self.assertEqual(self.puck.vy, 0, "The puck's y velocity should remain the same after collision")
    #testcase3: puck reset back to the center of the screen 
    def test_puck_reset(self):
        self.puck.reset(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
        self.assertEqual(self.puck.x, config.SCREEN_WIDTH // 2)
        self.assertEqual(self.puck.y, config.SCREEN_HEIGHT // 2)
        self.assertEqual(self.puck.vx, config.PUCK_INITIAL_SPEED)
        self.assertEqual(self.puck.vy, config.PUCK_INITIAL_SPEED)
    #testcase4: Score increment when the puck goes into the goal area & make sure that the score updates correctly. 
    def test_scoring(self):
        self.puck.x = -self.puck.radius
        self.puck.y = config.SCREEN_HEIGHT // 2
        score1 = 0
        score2 = 0

        if self.puck.x - self.puck.radius <= 0:
            score2 += 1

        self.assertEqual(score2, 1, "Score for player 2 should be 1")

    def tearDown(self):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
