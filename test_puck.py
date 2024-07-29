import pytest
from puck import Puck
from paddle import Paddle
import config
 
@pytest.fixture
def puck():
    return Puck(50, 50, 5, (255, 255, 255), 5)
 
@pytest.fixture
def paddle():
    return Paddle(45, 45, 10, 10, (255, 0, 0), 5)
 
def test_horizontal_collision(puck, paddle):
    puck.vx = 5
    puck.vy = 0
    paddle.vx = 0
    paddle.vy = 0
    assert puck.check_collision_with_paddle(paddle)
    assert puck.vx == 5 * config.PUCK_SPEED_INCREASE
    assert puck.vy == 0
 
def test_vertical_collision(puck, paddle):
    puck.vx = 0
    puck.vy = 5
    paddle.vx = 0
    paddle.vy = 0
    assert puck.check_collision_with_paddle(paddle)
    assert puck.vx == 0
    assert puck.vy == -5 * config.PUCK_SPEED_INCREASE
 
def test_paddle_movement_influence(puck, paddle):
    puck.vx = 5
    puck.vy = 0
    paddle.vx = 5
    paddle.vy = 0
    assert puck.check_collision_with_paddle(paddle)
    assert puck.vx == (5 * config.PUCK_SPEED_INCREASE) + (5 * 0.5)
    assert puck.vy == 0