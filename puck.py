import pygame
import config
from typing import Tuple


class Puck:
    def __init__(
        self,
        x: int,
        y: int,
        radius: int,
        color: Tuple[int, int, int],
        initial_speed: float,
    ) -> None:
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.radius = radius
        self.color = color
        self.vx = initial_speed
        self.vy = initial_speed
        self.started = False

    def start(self):
        self.vx = config.PUCK_INITIAL_SPEED
        self.vy = config.PUCK_INITIAL_SPEED
        self.started = True

    def update(self, screen_width: int, screen_height: int) -> None:
        if self.started:
            self.x += self.vx
            self.y += self.vy

            if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
                self.vx = -self.vx

            if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
                self.vy = -self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def check_collision_with_paddle(self, paddle):
        if self.is_colliding_with_paddle(paddle):
            overlap_x, overlap_y = self.calculate_overlap(paddle)
            self.resolve_collision(overlap_x, overlap_y, paddle)
            return True
        return False

    def is_colliding_with_paddle(self, paddle) -> bool:
        return (
            self.x + self.radius > paddle.x
            and self.x - self.radius < paddle.x + paddle.width
            and self.y + self.radius > paddle.y
            and self.y - self.radius < paddle.y + paddle.height
        )

    def calculate_overlap(self, paddle) -> Tuple[float, float]:
        overlap_x = min(
            self.x + self.radius - paddle.x,
            paddle.x + paddle.width - (self.x - self.radius),
        )
        overlap_y = min(
            self.y + self.radius - paddle.y,
            paddle.y + paddle.height - (self.y - self.radius),
        )
        return overlap_x, overlap_y

    def resolve_collision(self, overlap_x, overlap_y, paddle):
        if overlap_x < overlap_y:
            self.vx = -self.vx * config.PUCK_SPEED_INCREASE
            self.x += self.vx
        else:
            self.vy = -self.vy * config.PUCK_SPEED_INCREASE
            self.y += self.vy

        self.vx += paddle.vx * 0.5
        self.vy += paddle.vy * 0.5

    def reset(self, x=None, y=None):
        if x is None:
            x = self.initial_x
        if y is None:
            y = self.initial_y
        self.x = x
        self.y = y
        self.vx = config.PUCK_INITIAL_SPEED
        self.vy = config.PUCK_INITIAL_SPEED
        self.started = False
