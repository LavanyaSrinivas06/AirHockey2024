import pytest
from paddle import Paddle

# Configuration for test
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 80
PADDLE_COLOR = (255, 255, 255)
PADDLE_SPEED = 8

@pytest.fixture
def paddle():
    # Create a paddle instance
    return Paddle(8, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_COLOR, PADDLE_SPEED)

def test_paddle_initial_position(paddle):
    # Test the initial position of the paddle
    assert paddle.x == 8
    assert paddle.y == (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2

def test_paddle_reset(paddle):
    # Move the paddle and then reset it
    paddle.move_up()
    paddle.update(SCREEN_WIDTH, SCREEN_HEIGHT, 0, SCREEN_WIDTH)
    paddle.reset()
    # Test if the paddle position and velocity are reset
    assert paddle.x == paddle.initial_x
    assert paddle.y == paddle.initial_y
    assert paddle.vx == 0
    assert paddle.vy == 0

def test_paddle_move_left(paddle):
    initial_x = paddle.x
    paddle.move_left()
    paddle.update(SCREEN_WIDTH, SCREEN_HEIGHT, 0, SCREEN_WIDTH)
    assert paddle.x < initial_x

def test_paddle_move_right(paddle):
    initial_x = paddle.x
    paddle.move_right()
    paddle.update(SCREEN_WIDTH, SCREEN_HEIGHT, 0, SCREEN_WIDTH)
    assert paddle.x > initial_x

def test_paddle_move_up(paddle):
    initial_y = paddle.y
    paddle.move_up()
    paddle.update(SCREEN_WIDTH, SCREEN_HEIGHT, 0, SCREEN_WIDTH)
    assert paddle.y < initial_y

def test_paddle_move_down(paddle):
    initial_y = paddle.y
    paddle.move_down()
    paddle.update(SCREEN_WIDTH, SCREEN_HEIGHT, 0, SCREEN_WIDTH)
    assert paddle.y > initial_y
