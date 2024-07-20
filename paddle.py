import pygame
import config


class Paddle:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.vx = 0  # Initial velocity in x direction
        self.vy = 0  # Initial velocity in y direction

    def move_left(self):
        self.vx = -self.speed

    def move_right(self):
        self.vx = self.speed

    def move_up(self):
        self.vy = -self.speed

    def move_down(self):
        self.vy = self.speed

    def stop_horizontal(self):
        self.vx = 0

    def stop_vertical(self):
        self.vy = 0

    def update(self, screen_width, screen_height, left_bound, right_bound):
        self.x += self.vx
        self.y += self.vy

        # Prevent the paddle from moving out of the screen
        if self.x < left_bound:
            self.x = left_bound
        elif self.x + self.width > right_bound:
            self.x = right_bound - self.width

        if self.y < 0:
            self.y = 0
        elif self.y + self.height > screen_height:
            self.y = screen_height - self.height

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
