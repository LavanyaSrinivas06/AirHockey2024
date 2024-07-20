""" class for background in air hockey game"""

import pygame


class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = (0, 128, 128)  # Teal background color
        self.line_color = (255, 255, 255)  # White lines

    def update(self):
        # For now, no update logic is needed for the background
        pass

    def draw(self, surface):
        # Fill the background with the background color
        surface.fill(self.color)

        # Draw the center line
        pygame.draw.line(
            surface,
            self.line_color,
            (self.width // 2, 0),
            (self.width // 2, self.height),
            5,
        )

        # Draw the goal areas
        pygame.draw.rect(
            surface,
            self.line_color,
            pygame.Rect(0, (self.height // 2) - 100, 50, 200),
            5,
        )
        pygame.draw.rect(
            surface,
            self.line_color,
            pygame.Rect(self.width - 50, (self.height // 2) - 100, 50, 200),
            5,
        )
