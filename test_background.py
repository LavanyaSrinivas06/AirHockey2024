import pytest
import pygame
from background import Background  

@pytest.fixture
def background():
    width = 800
    height = 800
    return Background(width, height)

def test_initialization(background):
    assert background.width == 800
    assert background.height == 800
    assert background.color == (0, 128, 128)
    assert background.line_color == (255, 255, 255)

def test_draw(background):
    # Initialize Pygame to create a surface
    pygame.init()
    surface = pygame.Surface((background.width, background.height))

    # Call the draw method
    background.draw(surface)

    # Test if the surface has the background color 
    assert surface.get_at((0,128)) == background.color

    # Test if the center line and goal areas are drawn
    assert surface.get_at((background.width//2,0)) == background.line_color
    assert surface.get_at((0,(background.height // 2) - 100)) == background.line_color
    assert surface.get_at((background.width - 50,(background.height // 2) - 100)) == background.line_color

def test_update(background):
    background.update()
